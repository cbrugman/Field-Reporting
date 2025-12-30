from difflib import SequenceMatcher
import database

def find_matches(input_name, threshold=0.85, allowed_categories=None):
    """
    Returns (exact_match_species, list_of_fuzzy_matches)
    
    fuzzy_matches = [(species_obj, score), ...]
    """
    clean_input = input_name.strip()
    
    conn = database.get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM species')
    all_species = c.fetchall()
    conn.close()
    
    # Filter by category if specified
    if allowed_categories:
        all_species = [sp for sp in all_species if sp['category'] in allowed_categories]
    
    exact_match = None
    fuzzy_matches = []
    
    for sp in all_species:
        db_name = sp['common_name']
        
        # Helper to normalize (replace hyphens with spaces, remove punctuation)
        def normalize_name(s):
            return s.lower().replace('-', ' ').replace(',', '').replace('.', '').strip()

        # 1. Exact Match (Case insensitive)
        if db_name.lower() == clean_input.lower():
            exact_match = sp
            break # Exact match found
            
        # 1b. Normalized Exact Match (e.g. "sow-thistle" == "sow thistle")
        if normalize_name(db_name) == normalize_name(clean_input):
            exact_match = sp
            break
            
        # 2. Fuzzy Match
        ratio = SequenceMatcher(None, db_name.lower(), clean_input.lower()).ratio()
        
        # Check substring (input in db_name OR db_name in input)
        is_substring = clean_input.lower() in db_name.lower() or db_name.lower() in clean_input.lower()
        
        # Check Shared Words (e.g. "Great Mullein" vs "Common Mullein")
        word_match = False
        if not is_substring: # Optimization: Don't check words if whole string matches
            input_words = set(clean_input.lower().split())
            
            # Add singular forms for plural words (e.g. "chickadees" -> "chickadee")
            singular_words = set()
            for w in input_words:
                if w.endswith('s') and len(w) > 3:
                    singular_words.add(w[:-1])
            input_words.update(singular_words)
            
            db_words = set(db_name.lower().split())
            # Find intersection of words longer than 3 chars (ignores 'the', 'and', etc)
            shared_words = {w for w in input_words.intersection(db_words) if len(w) > 3}
            if shared_words:
                word_match = True

        # Include if ratio matches, substring, or shared words
        if ratio >= threshold or (is_substring and len(clean_input) > 3) or word_match:
            # Assign a base score for word match if ratio is low
            final_score = ratio
            if word_match and ratio < 0.6:
                final_score = 0.6 # Ensure it's enough to be seen but not 'High Match'

            fuzzy_matches.append({
                'id': sp['id'],
                'common_name': sp['common_name'],
                'score': round(final_score, 2)
            })
            
    # Sort fuzzy matches by score high->low
    fuzzy_matches.sort(key=lambda x: x['score'], reverse=True)
    
    return exact_match, fuzzy_matches
    
# Quick Test
if __name__ == "__main__":
    print("Testing 'Blue Jya'...")
    exact, fuzzy = find_matches("Blue Jya")
    print("Exact:", exact['common_name'] if exact else "None")
    print("Fuzzy:", fuzzy)
