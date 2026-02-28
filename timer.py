import streamlit as st
import time


def time_display(time_in_seconds):
    mins, secs = divmod(time_in_seconds, 60)
    time_now = '{:02d}:{:02d}'.format(mins, secs)
    st.title(f'{time_now}')
    time.sleep(1)
    return time_in_seconds - 1  # Return the updated value of time_in_seconds

def main(time_in_minutes=25):
    # For testing: 1 'minute' = 10 seconds
    og_time_in_seconds = time_in_minutes * 10
    session_state = st.session_state
    session_state.paused = session_state.get('paused', False)
    session_state.stopped = session_state.get('stopped', False)
    session_state.t_state = session_state.get('t_state', 'stopped')
    session_state.timer_widget = session_state.get('timer_widget', 'stopped_widget')

    timer_widget = session_state.timer_widget
    t_state = session_state.t_state

    # Always use the current input value for timer
    time_in_seconds = og_time_in_seconds

    buff1, col2, col3, buff2 = st.columns([1,3,3,1])
    with col2: 
        st.button("Stop", on_click=lambda: session_state.update(timer_widget='stopped_widget'))
    with col3:
        st.button("Start", on_click=lambda: session_state.update(timer_widget='counter_widget'))
    if timer_widget == 'stopped_widget':
        # Always reset to the current input value
        time_in_seconds = og_time_in_seconds
        session_state.stopped = True
        time_display(time_in_seconds)
    if timer_widget == 'counter_widget':
        with st.empty():
            while time_in_seconds:
                time_in_seconds = time_display(time_in_seconds)
                print(f'inside while loop: {time_in_seconds}')
            # Timer finished
            session_state.timer_completed = True
            st.rerun()
    return session_state.stopped
    

if __name__ == "__main__":
    timer_time = time_input()
    main(timer_time)


