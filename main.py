import time, datetime
import streamlit as st
from openai import OpenAI

# Configure Streamlit page and state
st.set_page_config(
    page_title="SpeechWriter",
    page_icon="./logo.ico",
    layout="centered"
)
tooltip_style = """
<style>
div[data-baseweb="tooltip"] {
  width: 300px;
}
</style>
"""
st.markdown(
    tooltip_style,
    unsafe_allow_html=True
)
st.markdown("")

def main():
    if check_password(st.session_state, st.secrets):
        if 'client' not in st.session_state:
            st.session_state['client'] = OpenAI(api_key=st.secrets['openai_key'])
            st.session_state['assistant_id'] = st.secrets['assistant_id']
            st.session_state['revise_mode'] = False
        # Main page
        if st.session_state['revise_mode']:
            revise()
        else:
            gather_info()


def check_password(state, secret):
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if state["password"] in secret["password"]:
            state["password_correct"] = True
            del state["password"]  # don't store password
        else:
            state["password_correct"] = False

    if "password_correct" not in state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password",
            placeholder='***********',
            help="""
            Right key, you do not have. Master Jun, you must seek.
            """
        )
        return False
    elif not state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


def gather_info():
    # Title of the web app
    st.title("Speech Writer")

    st.write("Hello! I'm an AI agent trained to help you draft a speech. I hope I am useful for you, but I must "
             "admit that I'm not perfect and I make mistakes. So please check the draft I wrote before you use "
             "it for any purpose. Please fill out some information below. Include as much detail as possible.")
    st.divider()
    # Text input box for project information
    event_name = st.text_input(
        "Name of event:",
        placeholder="e.g. Ribbon Cutting Ceremony of MetroLink Expansion Initiative",
        help="Enter the name or title of the event in which the speech will be delivered."
    )
    speech_length = st.text_input(
        "Length of Speech:",
        placeholder='e.g. 10 minutes long; not more 250 words; 30 minutes long with 5 minutes Q&A at 15 minutes mark',
        help="Determine the desired length of the speech and any time constraints that need to be adhered to. This "
             "will help you structure the speech effectively and ensure that it fits within the allotted time."
    )

    speech_audience = st.text_area(
        "Purpose and audience:",
        placeholder="e.g The transit event celebrates the launch of a new public transportation initiative, focusing "
                    "on improving accessibility and sustainability within our city. Attendees include residents, "
                    "business owners, policymakers, transportation advocates, and media representatives. The event "
                    "aims to highlight initiative benefits, foster community engagement, and garner support for "
                    "future transit projects. It aims to unites stakeholders from various sectors to recognize "
                    "collaborative efforts in achieving this vision.",
        help="Understand the purpose of the speech and who the intended audience is. What message does the speaker "
             "want to convey, and what action or response do they hope to elicit from the audience?"
    )
    project_info = st.text_area(
        "Project Information (Optional):",
        placeholder="e.g. MetroLink Expansion Initiative in Arcadia City is a comprehensive transit project set to "
                    "revolutionize urban mobility. With an estimated cost of $1.5 billion, this initiative "
                    "encompasses the construction of new subway lines, additional bus routes, modernized ticketing "
                    "systems, and bike-sharing programs, all aimed at providing residents with enhanced "
                    "transportation options. Funded through federal grants, private investments, and municipal bonds, "
                    "the project is anticipated to be completed over five years. Its benefits include reduced traffic "
                    "congestion, environmental sustainability, economic growth, social equity, and improved quality "
                    "of life. By fostering easier access to employment centers, educational institutions, "
                    "and cultural attractions, the MetroLink Expansion Initiative promises a cleaner, more connected, "
                    "and prosperous future for Arcadia City.",
        help="If this is for a specific project, please enter the project information here. Be sure to include scope, "
             "cost, benefit, etc. information."
    )

    speaker_background = st.text_area(
        "Speaker's background (Optional):",
        placeholder="e.g. Mark Stevens is the visionary Team Lead orchestrating the groundbreaking "
                    "Nexus Transit Project. Armed with a master's degree in Civil Engineering from the prestigious "
                    "Arcadia University, Mark's career spans two decades of innovation in transit infrastructure "
                    "development. His crowning achievement came with the seamless execution of the SkyBridge "
                    "Initiative, which revolutionized commuter connectivity in the region. Beyond his professional "
                    "pursuits, Mark is an avid cyclist who finds solace in exploring scenic routes during weekends, "
                    "fostering a deep appreciation for sustainable modes of transportation. Inspired by a childhood "
                    "fascination with model trains, Mark's commitment to excellence and his team's camaraderie are "
                    "driving forces propelling the Nexus Transit Project towards success.",
        help="Gather information about the speaker's background, expertise, and experiences relevant to the topic of "
             "the speech. This includes their education, career, achievements, and any personal anecdotes or stories "
             "they may want to share."
    )

    tone_style = st.text_area(
        "Tone and style (Optional):",
        placeholder="e.g. The tone of the speech should be authoritative yet approachable, conveying confidence and "
                    "expertise while remaining accessible to a diverse audience. The style should be engaging and "
                    "conversational, incorporating anecdotes and humor to connect with listeners on a personal level "
                    "and keep them actively engaged throughout the presentation.",
        help=("Determine the tone and style that the speaker prefers. Are they aiming for a formal, professional"
              "tone, or do they prefer a more conversational and approachable style? Understanding their "
              "preferences will help tailor the speech accordingly.")
    )

    quote_reference = st.text_area(
        "Quotes and references (Optional):",
        placeholder='e.g. "Investment in public transportation creates jobs, helps businesses grow, and provides people'
                    'with access to opportunity." - Anthony Foxx, Former United States Secretary of Transportation',
        help=("Enter here any specific quotes, references, or sources that the speaker wants to incorporate "
              "into the speech. These could be from influential figures, research studies, or other sources "
              "that support their message.")
    )

    if st.button("Submit", key="get_info_submit", type="primary"):
        # Processing logic here
        if not event_name:
            st.error("Please enter the event name.")
        if not speech_length:
            st.error("Please enter the speech length.")
        if not speech_audience:
            st.error("Please enter a Purpose and Audience description.")
        if event_name and speech_length and speech_audience:
            st.session_state['revise_mode'] = True
            st.session_state['user_input'] = dict(
                event_name=event_name,
                speech_length=speech_length,
                speech_audience=speech_audience,
                project_info=project_info,
                speaker_background=speaker_background,
                tone_style=tone_style,
                quote_reference=quote_reference
            )
            # create the thread
            thread = st.session_state['client'].beta.threads.create()
            st.session_state['thread_id'] = thread.id
            # create the first message
            message = "Help me write a speech based on the following parameters:  \n"
            for key, val in st.session_state['user_input'].items():
                message += "#" + key + "#" + ": " + val + "  \n"
            with st.spinner("Please wait while I draft the speech..."):
                st.session_state['speech'] = get_speech(message, st.session_state['thread_id'])
            st.session_state['data'] = [key + ': ' + val for key, val in st.session_state['user_input'].items()]
            st.session_state['data'].append('-----------------------------')
            st.session_state['data'].append(st.session_state['speech'])
            st.session_state['data'].append('-----------------------------')
            st.rerun()


def get_speech(message, thread_id):
    client = st.session_state['client']
    assistant_id = st.session_state['assistant_id']
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(2)  # Wait for 2 second
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            limit=1
        )
    else:
        st.write(run.status)

    # for msg in messages:
    #     st.write(msg.role + ':', msg.content[0].text.value)
    return messages.data[0].content[0].text.value


def revise():
    st.write(st.session_state['speech'])
    feedback = st.text_area(
        "Feedback:",
        placeholder="e.g. Give me another version. The speech is too long. Make it shorter. Remove the 3rd paragraph. "
                    "Combine and condense the last two paragraph. Use a lighter tone. Finish with a joke in the last "
                    "sentence of 4th paragraph.",
        help="Please provide your feedback. I will use your feedback to revise the draft."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Submit", key="revise_submit", type="primary"):
            if not feedback:
                st.error("Please enter the feedback.")
            else:
                with st.spinner("Please wait while I make the revision..."):
                    st.session_state['speech'] = get_speech(feedback, st.session_state['thread_id'])
                st.session_state['data'].append('feedback: ' + feedback)
                st.session_state['data'].append('-----------------------------')
                st.session_state['data'].append(st.session_state['speech'])
                st.session_state['data'].append('-----------------------------')
                st.rerun()
                revise()
    with col2:
        st.download_button(
            'Download',
            '  \n\n'.join(st.session_state['data'][::-1]),
            file_name=f'speech_{datetime.datetime.now().strftime("%H%M%S")}.txt',
            type="primary",
            key='download'
        )
    with col3:
        if st.button("Reset", key="reset_submit", type="primary"):
            st.session_state['revise_mode'] = False
            st.rerun()


if __name__ == "__main__":
    main()
