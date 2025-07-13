"""Unit tests for graceful shutdown handler."""

import pytest
import signal
from unittest.mock import patch, MagicMock, call

from shutdown_handler import GracefulShutdown


class TestGracefulShutdown:
    """Test graceful shutdown functionality."""

    def test_init_default_logger(self):
        """Test initialization with default logger."""
        shutdown = GracefulShutdown()
        
        assert shutdown.logger is not None
        assert shutdown.shutdown_callbacks == []
        assert shutdown.is_shutting_down is False

    def test_init_custom_logger(self):
        """Test initialization with custom logger."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        
        assert shutdown.logger == mock_logger

    @patch('shutdown_handler.signal.signal')
    def test_signal_handlers_registered(self, mock_signal):
        """Test that signal handlers are properly registered."""
        shutdown = GracefulShutdown()
        
        # Check that signal handlers were registered
        expected_calls = [
            call(signal.SIGINT, shutdown._handle_shutdown),
            call(signal.SIGTERM, shutdown._handle_shutdown),
        ]
        
        # SIGBREAK is Windows-specific
        if hasattr(signal, 'SIGBREAK'):
            expected_calls.append(call(signal.SIGBREAK, shutdown._handle_shutdown))
        
        mock_signal.assert_has_calls(expected_calls, any_order=True)

    def test_register_callback(self):
        """Test registering shutdown callbacks."""
        shutdown = GracefulShutdown()
        
        def test_callback(arg1, arg2, kwarg1=None):
            pass
        
        shutdown.register(test_callback, "arg1_value", "arg2_value", kwarg1="kwarg1_value")
        
        assert len(shutdown.shutdown_callbacks) == 1
        callback, args, kwargs = shutdown.shutdown_callbacks[0]
        assert callback == test_callback
        assert args == ("arg1_value", "arg2_value")
        assert kwargs == {"kwarg1": "kwarg1_value"}

    def test_register_multiple_callbacks(self):
        """Test registering multiple shutdown callbacks."""
        shutdown = GracefulShutdown()
        
        def callback1():
            pass
        
        def callback2():
            pass
        
        shutdown.register(callback1)
        shutdown.register(callback2)
        
        assert len(shutdown.shutdown_callbacks) == 2

    @patch('shutdown_handler.os._exit')
    @patch('builtins.print')
    def test_handle_shutdown_first_signal(self, mock_print, mock_exit):
        """Test handling first shutdown signal."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        
        callback_called = []
        
        def test_callback():
            callback_called.append(True)
        
        shutdown.register(test_callback)
        
        # Simulate SIGINT
        shutdown._handle_shutdown(signal.SIGINT, None)
        
        # Check that callback was called
        assert len(callback_called) == 1
        assert shutdown.is_shutting_down is True
        
        # Check logging
        mock_logger.info.assert_called()
        mock_logger.debug.assert_called()
        
        # Check exit
        mock_exit.assert_called_once_with(0)

    @patch('shutdown_handler.os._exit')
    @patch('builtins.print')
    def test_handle_shutdown_second_signal(self, mock_print, mock_exit):
        """Test handling second shutdown signal (force exit)."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        shutdown.is_shutting_down = True  # Already shutting down
        
        # Simulate second signal
        shutdown._handle_shutdown(signal.SIGTERM, None)
        
        # Should force exit with code 1
        mock_exit.assert_any_call(1)
        mock_logger.warning.assert_called()

    @patch('shutdown_handler.os._exit')
    @patch('builtins.print')
    def test_handle_shutdown_callback_error(self, mock_print, mock_exit):
        """Test handling shutdown when callback raises exception."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        
        def failing_callback():
            raise Exception("Callback failed")
        
        def working_callback():
            pass
        
        shutdown.register(failing_callback)
        shutdown.register(working_callback)
        
        # Should handle the error and continue
        shutdown._handle_shutdown(signal.SIGINT, None)
        
        # Should have logged the error
        mock_logger.error.assert_called()
        
        # Should still exit normally
        mock_exit.assert_called_once_with(0)

    @patch('shutdown_handler.os._exit')
    @patch('builtins.print')
    def test_handle_shutdown_callbacks_executed_in_reverse_order(self, mock_print, mock_exit):
        """Test that callbacks are executed in reverse registration order."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        
        execution_order = []
        
        def callback1():
            execution_order.append(1)
        
        def callback2():
            execution_order.append(2)
        
        def callback3():
            execution_order.append(3)
        
        # Register in order 1, 2, 3
        shutdown.register(callback1)
        shutdown.register(callback2)
        shutdown.register(callback3)
        
        shutdown._handle_shutdown(signal.SIGINT, None)
        
        # Should execute in reverse order: 3, 2, 1
        assert execution_order == [3, 2, 1]

    @patch('shutdown_handler.os._exit')
    @patch('builtins.print')
    def test_handle_shutdown_with_callback_arguments(self, mock_print, mock_exit):
        """Test shutdown handling with callback arguments."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        
        callback_args = []
        
        def test_callback(arg1, arg2, kwarg1=None, kwarg2=None):
            callback_args.extend([arg1, arg2, kwarg1, kwarg2])
        
        shutdown.register(test_callback, "pos1", "pos2", kwarg1="kw1", kwarg2="kw2")
        
        shutdown._handle_shutdown(signal.SIGINT, None)
        
        assert callback_args == ["pos1", "pos2", "kw1", "kw2"]

    @patch('shutdown_handler.signal.Signals')
    @patch('shutdown_handler.os._exit')
    @patch('builtins.print')
    def test_signal_name_handling(self, mock_print, mock_exit, mock_signals):
        """Test signal name extraction for logging."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        
        # Mock signal name
        mock_signal = MagicMock()
        mock_signal.name = "SIGINT"
        mock_signals.return_value = mock_signal
        
        shutdown._handle_shutdown(signal.SIGINT, None)
        
        # Should log with signal name
        log_calls = mock_logger.info.call_args_list
        assert any("SIGINT" in str(call) for call in log_calls)

    @patch('shutdown_handler.os._exit')
    @patch('builtins.print')
    def test_signal_name_fallback(self, mock_print, mock_exit):
        """Test signal name fallback when signal.Signals not available."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        
        # Temporarily remove Signals attribute from signal module
        original_signals = getattr(signal, 'Signals', None)
        if hasattr(signal, 'Signals'):
            delattr(signal, 'Signals')
        
        try:
            shutdown._handle_shutdown(signal.SIGINT, None)
        finally:
            # Restore Signals attribute if it existed
            if original_signals is not None:
                signal.Signals = original_signals
        
        # Should still work and log with signal number
        mock_logger.info.assert_called()
        log_calls = mock_logger.info.call_args_list
        assert any(str(signal.SIGINT) in str(call) for call in log_calls)

    def test_callback_registration_with_no_args(self):
        """Test callback registration with no arguments."""
        shutdown = GracefulShutdown()
        
        def simple_callback():
            pass
        
        shutdown.register(simple_callback)
        
        callback, args, kwargs = shutdown.shutdown_callbacks[0]
        assert callback == simple_callback
        assert args == ()
        assert kwargs == {}

    def test_empty_shutdown(self):
        """Test shutdown with no registered callbacks."""
        with patch('shutdown_handler.os._exit') as mock_exit, \
             patch('builtins.print'):
            
            mock_logger = MagicMock()
            shutdown = GracefulShutdown(logger=mock_logger)
            
            shutdown._handle_shutdown(signal.SIGINT, None)
            
            # Should still work and exit normally
            mock_exit.assert_called_once_with(0)
            mock_logger.info.assert_called()

    @patch('shutdown_handler.os._exit')
    @patch('builtins.print')
    def test_callback_with_side_effects(self, mock_print, mock_exit):
        """Test callback that has side effects."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        
        side_effects = []
        
        def callback_with_side_effects():
            side_effects.append("cleanup_performed")
            # Simulate file cleanup, connection closing, etc.
            return "cleanup_result"
        
        shutdown.register(callback_with_side_effects)
        
        shutdown._handle_shutdown(signal.SIGINT, None)
        
        assert "cleanup_performed" in side_effects

    @patch('shutdown_handler.os._exit')
    @patch('builtins.print')
    def test_multiple_callback_errors(self, mock_print, mock_exit):
        """Test handling multiple callback errors."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        
        def failing_callback_1():
            raise ValueError("Error 1")
        
        def failing_callback_2():
            raise RuntimeError("Error 2")
        
        def working_callback():
            pass
        
        shutdown.register(failing_callback_1)
        shutdown.register(working_callback)
        shutdown.register(failing_callback_2)
        
        shutdown._handle_shutdown(signal.SIGINT, None)
        
        # Should have logged both errors
        error_calls = mock_logger.error.call_args_list
        assert len(error_calls) == 2
        
        # Should still exit normally
        mock_exit.assert_called_once_with(0)

    def test_shutdown_state_management(self):
        """Test shutdown state management."""
        shutdown = GracefulShutdown()
        
        assert shutdown.is_shutting_down is False
        
        with patch('shutdown_handler.os._exit'), \
             patch('builtins.print'):
            
            shutdown._handle_shutdown(signal.SIGINT, None)
            assert shutdown.is_shutting_down is True


@pytest.mark.integration
class TestShutdownIntegration:
    """Integration tests for shutdown handler."""

    def test_shutdown_handler_in_context(self):
        """Test shutdown handler usage in realistic context."""
        cleanup_performed = []
        
        def cleanup_database():
            cleanup_performed.append("database")
        
        def cleanup_files():
            cleanup_performed.append("files")
        
        def cleanup_network():
            cleanup_performed.append("network")
        
        shutdown_handler = GracefulShutdown()
        shutdown_handler.register(cleanup_database)
        shutdown_handler.register(cleanup_files)
        shutdown_handler.register(cleanup_network)
        
        with patch('shutdown_handler.os._exit'), \
             patch('builtins.print'):
            
            # Simulate shutdown
            shutdown_handler._handle_shutdown(signal.SIGTERM, None)
            
            # All cleanup should have been performed in reverse order
            assert cleanup_performed == ["network", "files", "database"]

    def test_resource_cleanup_scenario(self):
        """Test realistic resource cleanup scenario."""
        resources = {
            "database_connection": True,
            "file_handles": True,
            "network_sockets": True,
            "temp_files": True
        }
        
        def cleanup_resources():
            resources["database_connection"] = False
            resources["file_handles"] = False
            resources["network_sockets"] = False
            resources["temp_files"] = False
        
        shutdown_handler = GracefulShutdown()
        shutdown_handler.register(cleanup_resources)
        
        with patch('shutdown_handler.os._exit'), \
             patch('builtins.print'):
            
            shutdown_handler._handle_shutdown(signal.SIGINT, None)
            
            # All resources should be cleaned up
            assert all(not active for active in resources.values())

    def test_shutdown_with_failing_and_succeeding_cleanup(self):
        """Test mixed success/failure cleanup scenario."""
        cleanup_status = {}
        
        def critical_cleanup():
            cleanup_status["critical"] = "success"
        
        def failing_cleanup():
            cleanup_status["failing"] = "attempted"
            raise Exception("Cleanup failed")
        
        def optional_cleanup():
            cleanup_status["optional"] = "success"
        
        shutdown_handler = GracefulShutdown()
        shutdown_handler.register(critical_cleanup)
        shutdown_handler.register(failing_cleanup)
        shutdown_handler.register(optional_cleanup)
        
        with patch('shutdown_handler.os._exit'), \
             patch('builtins.print'):
            
            shutdown_handler._handle_shutdown(signal.SIGINT, None)
            
            # Critical and optional should succeed, failing should be attempted
            assert cleanup_status["critical"] == "success"
            assert cleanup_status["failing"] == "attempted"
            assert cleanup_status["optional"] == "success"


class TestShutdownHandlerEdgeCases:
    """Test edge cases and error scenarios."""

    def test_callback_modifying_callback_list(self):
        """Test callback that tries to modify the callback list."""
        shutdown = GracefulShutdown()
        
        def modifying_callback():
            # Try to add another callback during shutdown
            def new_callback():
                pass
            shutdown.register(new_callback)
        
        shutdown.register(modifying_callback)
        
        with patch('shutdown_handler.os._exit'), \
             patch('builtins.print'):
            
            # Should not crash
            shutdown._handle_shutdown(signal.SIGINT, None)

    def test_callback_infinite_loop_protection(self):
        """Test protection against callback infinite loops."""
        shutdown = GracefulShutdown()
        
        call_count = [0]
        
        def recursive_callback():
            call_count[0] += 1
            if call_count[0] < 5:  # Prevent actual infinite loop in test
                # This would be bad in real code
                pass
        
        shutdown.register(recursive_callback)
        
        with patch('shutdown_handler.os._exit'), \
             patch('builtins.print'):
            
            shutdown._handle_shutdown(signal.SIGINT, None)
            
            # Should complete without hanging
            assert call_count[0] > 0

    @patch('shutdown_handler.os._exit')
    @patch('builtins.print')
    def test_callback_with_complex_exception(self, mock_print, mock_exit):
        """Test callback with complex exception handling."""
        mock_logger = MagicMock()
        shutdown = GracefulShutdown(logger=mock_logger)
        
        def complex_failing_callback():
            try:
                raise ValueError("Inner error")
            except ValueError as e:
                raise RuntimeError("Outer error") from e
        
        shutdown.register(complex_failing_callback)
        
        shutdown._handle_shutdown(signal.SIGINT, None)
        
        # Should handle complex exception chains
        mock_logger.error.assert_called()
        mock_exit.assert_called_once_with(0)

    def test_very_long_callback_list(self):
        """Test shutdown with many callbacks."""
        shutdown = GracefulShutdown()
        
        execution_count = [0]
        
        def counting_callback():
            execution_count[0] += 1
        
        # Register many callbacks
        for _ in range(100):
            shutdown.register(counting_callback)
        
        with patch('shutdown_handler.os._exit'), \
             patch('builtins.print'):
            
            shutdown._handle_shutdown(signal.SIGINT, None)
            
            # All callbacks should execute
            assert execution_count[0] == 100