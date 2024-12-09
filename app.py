from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
from datetime import datetime, timedelta
import random

app = FastAPI()
state_list = ['hostile', 'play', 'relax', 'whining']

# Global variable to keep track of the last request time from 'owner'
owner_last_request_time = None


@app.post("/")
async def classify_audio(
    user_id: str = Form(...),
    species: str = Form(...),
    file: UploadFile = File(...)
):
    global owner_last_request_time
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="No user_id provided")

        if not species:
            raise HTTPException(status_code=400, detail="No species provided")

        if not file or not file.filename:
            raise HTTPException(
                status_code=400, detail="No audio file provided")

        current_time = datetime.now()

        if user_id == 'owner':
            desired_state = None

            if not owner_last_request_time or (current_time - owner_last_request_time) > timedelta(minutes=3):
                desired_state = 'hostile'
            else:
                desired_state = 'whining'

            owner_last_request_time = current_time

            # Create a state list with desired_state first and others shuffled
            other_states = [
                state for state in state_list if state != desired_state]
            random.shuffle(other_states)
            states = [desired_state] + other_states

            # Assign values
            first_value = random.uniform(0.6, 0.9)
            remaining = 1 - first_value

            second_value_min = 0.1
            second_value_max = remaining
            if second_value_max < second_value_min:
                second_value_max = second_value_min
            second_value = random.uniform(second_value_min, second_value_max)

            remaining -= second_value

            if remaining <= 0:
                third_value = fourth_value = 0.0
            else:
                third_value = random.uniform(0, remaining)
                fourth_value = remaining - third_value

            values = [first_value, second_value, third_value, fourth_value]
            result = dict(zip(states, values))

            sorted_result = dict(
                sorted(result.items(), key=lambda item: item[1], reverse=True))

            return JSONResponse(content=sorted_result)
        else:
            # For other users
            states = state_list.copy()
            random.shuffle(states)

            first_value = random.uniform(0.6, 0.9)
            remaining = 1 - first_value

            second_value_min = 0.1
            second_value_max = remaining
            if second_value_max < second_value_min:
                second_value_max = second_value_min
            second_value = random.uniform(second_value_min, second_value_max)

            remaining -= second_value

            if remaining <= 0:
                third_value = fourth_value = 0.0
            else:
                third_value = random.uniform(0, remaining)
                fourth_value = remaining - third_value

            values = [first_value, second_value, third_value, fourth_value]
            result = dict(zip(states, values))

            sorted_result = dict(
                sorted(result.items(), key=lambda item: item[1], reverse=True))

            return JSONResponse(content=sorted_result)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    print("Starting FastAPI app...")
    uvicorn.run(app, host='0.0.0.0', port=7230)
# uvicorn app:app --host 0.0.0.0 --port 7230 --reload
