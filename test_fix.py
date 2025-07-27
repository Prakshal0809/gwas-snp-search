import requests
import time

def test_with_results():
    # Test with a search term that should return results
    print("Testing search for 'diabetes' (should return results)...")
    response = requests.post('http://localhost:5000/api/search', 
                           json={'search_term': 'diabetes'})
    print("Search started:", response.json())
    
    # Wait and check status
    for i in range(30):  # Wait up to 30 seconds
        time.sleep(2)
        status = requests.get('http://localhost:5000/api/status').json()
        print(f"Status ({i*2}s): {status}")
        
        if not status['is_running']:
            if status.get('no_results'):
                print("❌ ERROR: No results detected for 'diabetes' when it should have results!")
            elif status.get('error'):
                print(f"❌ ERROR: {status['error']}")
            elif status.get('filename'):
                print("✅ SUCCESS: Found results for 'diabetes'!")
                print(f"SNPs found: {status['count']}")
                print(f"Filename: {status['filename']}")
            else:
                print("❌ UNEXPECTED: Unknown status")
            break
    else:
        print("❌ Search timed out")

if __name__ == "__main__":
    test_with_results() 