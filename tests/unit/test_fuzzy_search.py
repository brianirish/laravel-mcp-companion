"""Tests for the fuzzy_search function."""

from laravel_mcp_companion import fuzzy_search


class TestFuzzySearch:
    """Test cases for fuzzy_search functionality."""
    
    def test_exact_match_single_word(self):
        """Test exact match for single word."""
        text = "Laravel is a PHP framework for web artisans"
        matches = fuzzy_search("Laravel", text)
        
        assert len(matches) > 0
        assert matches[0]['score'] == 1.0
        assert matches[0]['word'] == 'laravel'
        assert 'laravel' in matches[0]['context'].lower()
    
    def test_case_insensitive_match(self):
        """Test that matching is case insensitive."""
        text = "LARAVEL is great and laravel is powerful"
        matches = fuzzy_search("LaRaVeL", text)
        
        assert len(matches) == 2
        assert all(m['score'] == 1.0 for m in matches)
    
    def test_partial_match_above_threshold(self):
        """Test partial matches above threshold."""
        text = "Laravel, Lara, and Laravell are similar words"
        matches = fuzzy_search("Laravel", text, threshold=0.8)
        
        assert len(matches) >= 1
        assert any(m['word'] == 'laravel,' for m in matches)
        # Lara should not match with 0.8 threshold (too short)
        assert not any(m['word'] == 'lara,' for m in matches)
    
    def test_partial_match_with_lower_threshold(self):
        """Test partial matches with lower threshold."""
        text = "Laravel, Lara, and Laravell are similar words"
        matches = fuzzy_search("Laravel", text, threshold=0.5)
        
        assert len(matches) >= 2
        word_matches = [m['word'] for m in matches]
        assert 'lara,' in word_matches or 'lara' in word_matches
    
    def test_multi_word_query(self):
        """Test matching multi-word queries."""
        text = "The Laravel framework is a PHP framework for building web applications"
        matches = fuzzy_search("Laravel framework", text)
        
        assert len(matches) > 0
        assert matches[0]['score'] == 1.0
        assert matches[0]['word'] == 'laravel framework'
    
    def test_multi_word_partial_match(self):
        """Test partial matching of multi-word queries."""
        text = "Laravel is great and the Laravel ecosystem is vast"
        matches = fuzzy_search("Laravel ecosystem", text, threshold=0.7)
        
        assert len(matches) >= 1
        assert any('laravel ecosystem' in m['word'] for m in matches)
    
    def test_context_extraction(self):
        """Test that context is properly extracted around matches."""
        text = " ".join([f"word{i}" for i in range(30)])
        text += " Laravel " + " ".join([f"word{i}" for i in range(30, 60)])
        
        matches = fuzzy_search("Laravel", text)
        
        assert len(matches) == 1
        context_words = matches[0]['context'].split()
        # Should have ~20 words of context (10 before + match + 10 after)
        assert 15 <= len(context_words) <= 25
        assert 'laravel' in matches[0]['context'].lower()
    
    def test_position_calculation(self):
        """Test that position is correctly calculated."""
        text = "Hello world Laravel framework"
        matches = fuzzy_search("Laravel", text)
        
        assert len(matches) == 1
        # Position should be at the start of "Laravel" 
        # "Hello " (6) + "world " (6) = 12
        assert matches[0]['position'] == 12
    
    def test_empty_inputs(self):
        """Test handling of empty query and text."""
        # Empty query
        matches = fuzzy_search("", "Laravel is a PHP framework")
        assert len(matches) == 0
        
        # Empty text
        matches = fuzzy_search("Laravel", "")
        assert len(matches) == 0
    
    def test_query_longer_than_text(self):
        """Test when query is longer than the text."""
        text = "PHP"
        matches = fuzzy_search("Laravel Framework", text)
        
        assert len(matches) == 0
    
    def test_special_characters_in_query(self):
        """Test handling of special characters."""
        text = "Use Laravel's blade.php templates"
        matches = fuzzy_search("blade.php", text)
        
        assert len(matches) > 0
        assert any('blade.php' in m['word'] for m in matches)
    
    def test_sorting_by_score(self):
        """Test that results are sorted by score descending."""
        text = "Laravel is great, Lara is short, Laravell is close"
        matches = fuzzy_search("Laravel", text, threshold=0.5)
        
        assert len(matches) >= 2
        # Check that scores are in descending order
        scores = [m['score'] for m in matches]
        assert scores == sorted(scores, reverse=True)
    
    def test_unicode_handling(self):
        """Test handling of unicode characters."""
        text = "Laravel é ótimo para desenvolvimento"
        matches = fuzzy_search("é", text)
        
        assert len(matches) > 0
        assert matches[0]['word'] == 'é'
    
    def test_punctuation_handling(self):
        """Test handling of punctuation in text."""
        text = "Laravel, PHP, and MySQL: the perfect stack!"
        matches = fuzzy_search("Laravel", text)
        
        assert len(matches) > 0
        # Should match "Laravel," with comma
        assert any('laravel' in m['word'].lower() for m in matches)
    
    def test_threshold_boundary(self):
        """Test threshold boundary conditions."""
        text = "Lara is almost Laravel"
        
        # Just below threshold - no match (Lara vs Laravel is ~0.77)
        matches = fuzzy_search("Laravel", text, threshold=0.8)
        assert not any(m['word'] == 'lara' for m in matches)
        
        # Just above threshold - should match
        matches = fuzzy_search("Laravel", text, threshold=0.7)
        assert any(m['word'] == 'lara' for m in matches)
    
    def test_duplicate_words(self):
        """Test handling of duplicate words in text."""
        text = "Laravel Laravel Laravel is repeated"
        matches = fuzzy_search("Laravel", text)
        
        # Should find all three occurrences
        assert len(matches) == 3
        assert all(m['score'] == 1.0 for m in matches)
        # Check positions are different
        positions = [m['position'] for m in matches]
        assert len(set(positions)) == 3
    
    def test_performance_with_large_text(self):
        """Test performance doesn't degrade badly with large text."""
        import time
        
        # Create a large text (10,000 words)
        text = " ".join([f"word{i}" for i in range(10000)])
        text += " Laravel framework " 
        text += " ".join([f"word{i}" for i in range(10000, 20000)])
        
        start_time = time.time()
        matches = fuzzy_search("Laravel", text)
        end_time = time.time()
        
        assert len(matches) > 0
        # Should complete in reasonable time (< 1 second)
        assert end_time - start_time < 1.0