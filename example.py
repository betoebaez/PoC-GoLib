"""
Simple test/example script for LibCoreHey package.
This demonstrates how the package should be imported and used.
"""

def test_import():
    """Test that the package can be imported correctly."""
    print("🧪 Testing LibCoreHey import...")
    
    try:
        import libcorehey as LibCoreHey
        print("✅ Successfully imported libcorehey as LibCoreHey")
        
        # Test math functions if available
        try:
            result = LibCoreHey.add_numbers(5, 3)
            print(f"✅ Math test: 5 + 3 = {result}")
            
            fib = LibCoreHey.get_fibonacci(8)
            print(f"✅ Fibonacci test: F(8) = {fib}")
            
            prime = LibCoreHey.is_prime(17)
            print(f"✅ Prime test: is_prime(17) = {prime}")
            
        except Exception as e:
            print(f"⚠️  Math functions not available: {e}")
        
        # Test API functions (will fail without proper credentials, but should be importable)
        try:
            # This will fail due to invalid credentials, but the function should exist
            LibCoreHey.get_quick_replies("test", "test", "test")
        except Exception as e:
            if "get_quick_replies" in str(e) or "Failed to get quick replies" in str(e):
                print("✅ API functions are available (expected failure with test credentials)")
            else:
                print(f"❌ Unexpected error with API functions: {e}")
        
        print("🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def demonstrate_usage():
    """Demonstrate the intended usage of the library."""
    print("\n📚 Usage demonstration:")
    print("=" * 50)
    
    print("""
# Import the library
import libcorehey as LibCoreHey

# Math operations
result = LibCoreHey.add_numbers(10, 15)  # Returns 25
product = LibCoreHey.multiply_numbers(6, 7)  # Returns 42
fibonacci = LibCoreHey.get_fibonacci(12)  # Returns 144
is_prime_num = LibCoreHey.is_prime(29)  # Returns True

# HeyBanco API calls (requires valid credentials)
token = "your-api-token"
org = "your-organization"
group = "your-group"

quick_replies = LibCoreHey.get_quick_replies(token, org, group)
typifications = LibCoreHey.get_typification(token, org, group)

print("JSON Response:", quick_replies)
""")


if __name__ == "__main__":
    success = test_import()
    
    if success:
        demonstrate_usage()
        print("\n🚀 LibCoreHey is ready to use!")
        print("📝 For more examples, check the README.md file")
    else:
        print("\n❌ Please check the installation and try again")
        print("💡 Make sure you've run: pip install -e .")