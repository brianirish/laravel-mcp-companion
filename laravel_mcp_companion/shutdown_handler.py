import signal
import logging
import os
from typing import Callable, Optional, Any, List, Tuple

class GracefulShutdown:
    """
    Handles graceful shutdown of the server when receiving termination signals.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize the shutdown handler."""
        self.logger = logger or logging.getLogger(__name__)
        self.shutdown_callbacks: List[Tuple[Callable, tuple, dict]] = []
        self.is_shutting_down = False
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        
        # On Windows, SIGBREAK is sent on Ctrl+Break
        if hasattr(signal, 'SIGBREAK'):
            signal.signal(signal.SIGBREAK, self._handle_shutdown)
    
    def register(self, callback: Callable[[], Any], *args, **kwargs) -> None:
        """
        Register a callback to be executed during shutdown.
        
        Args:
            callback: Function to call during shutdown
            *args: Arguments to pass to the callback
            **kwargs: Keyword arguments to pass to the callback
        """
        self.shutdown_callbacks.append((callback, args, kwargs))
    
    def _handle_shutdown(self, sig, frame) -> None:
        """
        Handle termination signals by running registered callbacks.
        
        Args:
            sig: Signal number
            frame: Current stack frame
        """
        if self.is_shutting_down:
            # If we get another signal during shutdown, exit more forcefully
            self.logger.warning("Received second termination signal, forcing exit")
            os._exit(1)  # Use os._exit instead of sys.exit for more forceful termination
        
        self.is_shutting_down = True
        signal_name = signal.Signals(sig).name if hasattr(signal, 'Signals') else str(sig)
        
        self.logger.info(f"Received {signal_name}, shutting down gracefully...")
        print(f"\nReceived {signal_name}, shutting down gracefully...")
        
        # Run all registered callbacks in reverse order
        for callback, args, kwargs in reversed(self.shutdown_callbacks):
            try:
                self.logger.debug(f"Running shutdown callback: {callback.__name__}")
                callback(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error in shutdown callback {callback.__name__}: {str(e)}")
        
        self.logger.info("Shutdown complete")
        print("Shutdown complete")
        
        # Use os._exit for more reliable termination with FastMCP
        os._exit(0)
