import pytest
import httpx
import time
import asyncio

BASE_URL = "http://127.0.0.1:8000/api/refactoring"

# Sample Python code for testing
SAMPLE_PYTHON_CODE = """
def inefficient_sum(numbers):
    s = 0
    for n in numbers:
        s += n
    return s
"""

@pytest.mark.asyncio
async def test_create_and_get_refactoring():
    """
    Test the full refactoring lifecycle:
    1. Create a refactoring request.
    2. Poll the API until the status is 'completed'.
    3. Verify the final result.
    """
    async with httpx.AsyncClient() as client:
        # 1. Create a refactoring request
        create_payload = {
            "original_code": SAMPLE_PYTHON_CODE,
            "language": "python"
        }
        response = await client.post(BASE_URL + "/", json=create_payload)
        
        assert response.status_code == 200
        initial_data = response.json()
        assert "id" in initial_data
        assert initial_data["status"] == "processing"
        
        refactoring_id = initial_data["id"]
        
        # 2. Poll for the result
        start_time = time.time()
        timeout = 60  # 60-second timeout
        
        while time.time() - start_time < timeout:
            get_response = await client.get(f"{BASE_URL}/{refactoring_id}")
            assert get_response.status_code == 200
            result_data = get_response.json()
            
            if result_data["status"] == "completed":
                break
            elif result_data["status"] == "failed":
                pytest.fail(f"Refactoring failed with explanation: {result_data.get('explanation')}")
            
            await asyncio.sleep(2)  # Wait for 2 seconds before polling again
        else:
            pytest.fail("Refactoring process timed out.")

        # 3. Verify the final result
        assert result_data["status"] == "completed"
        assert "refactored_code" in result_data and result_data["refactored_code"]
        assert "explanation" in result_data and result_data["explanation"]
        assert result_data["original_code"] == SAMPLE_PYTHON_CODE
        
        # Check that the refactored code is different and sensible
        assert result_data["refactored_code"] != SAMPLE_PYTHON_CODE
        assert "sum(" in result_data["refactored_code"]  # Expecting the built-in sum() function

@pytest.mark.asyncio
async def test_get_nonexistent_refactoring():
    """Test retrieving a refactoring that does not exist."""
    async with httpx.AsyncClient() as client:
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"{BASE_URL}/{non_existent_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Refactoring not found" 