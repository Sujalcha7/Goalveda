import streamlit as st
import time

def count_down(ts, paused, stop):
    original_ts = ts
    with st.empty():
        while ts:
            if paused:
                continue  # Skip iteration if paused
            if stop:
                mins, secs = divmod(ts, 60)
                time_now = '{:02d}:{:02d}'.format(mins, secs)
                return st.title(f'{time_now}')
            if stop and paused:
                st.experimental_rerun()
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.title(f"{time_now}")
            time.sleep(1)
            ts -= 1

def time_input():
    time_minutes = st.number_input('Enter the time in minutes ', min_value=1, value=25)
    return time_minutes

def main(time_in_minutes=25):
    time_in_seconds = time_in_minutes * 60
    paused = False
    stop = False
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        if st.button("PAUSE", key="pause_button"):
            paused = not paused

        if st.button("STOP", key="stop_button"):
            stop = True

        count_down(int(time_in_seconds), paused, stop)

if __name__ == "__main__":
    main()