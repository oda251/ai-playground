import flet as ft
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import uuid
from simple_agent.agent import build_simple_agent
from typing import List

# configuration
APP_NAME = "simple_agent"
session_service = InMemorySessionService()


# util
def create_new_session(user_id: str) -> str:
    """Creates a new session."""
    id = str(uuid.uuid4())
    session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=id)
    return id


def delete_session(session_id: str, user_id: str):
    """Deletes a session."""
    session_service.delete_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )


def build_runnner(agent: Agent):
    """Builds the runner with the specified agent and session service."""
    return Runner(agent=agent, app_name=APP_NAME, session_service=session_service)


def create_request(query: str) -> types.Content:
    """Creates a request."""
    return types.Content(role="user", parts=[types.Part(text=query)])


def create_talk_card(query: str, reply: str) -> ft.Row:
    """Creates a talk card."""
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(value=query, weight=ft.FontWeight.BOLD, selectable=True),
                    ft.Text(reply, selectable=True),
                ],
            ),
            width=400,
            bgcolor=ft.colors.BLUE_100,
            padding=10,
            border_radius=ft.border_radius.all(10),
        )
    )


def main(page: ft.Page):
    page.title = "test app"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    USER_ID = "example_user"
    session_id = create_new_session(USER_ID)
    query = ft.TextField(label="Query", width=300)
    agent = build_simple_agent()
    runner = build_runnner(agent)
    log: List = []
    log_view = ft.ListView(
        col=ft.Colors.BLUE_50,
        width=400,
        height=400,
    )

    def on_new_session_click(e):
        nonlocal session_id
        nonlocal log
        if session_id and session_id != "":
            delete_session(session_id, USER_ID)
        session_id = create_new_session(USER_ID)
        log = []
        page.update()

    def on_query_submit(e):
        nonlocal log
        if query.value == "":
            return
        request = create_request(query.value)
        for event in runner.run(
            user_id=USER_ID, session_id=session_id, new_message=request
        ):
            if event.is_final_response:
                res = event.content.parts[0].text
                log_view.controls.append(create_talk_card(query.value, res))
                query.value = ""
                page.update()
                break
        query.value = ""
        page.update()

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        query,
                        ft.ElevatedButton("Submit", on_click=on_query_submit),
                        ft.ElevatedButton("New Session", on_click=on_new_session_click),
                    ]
                ),
                log_view,
            ]
        )
    )


ft.app(main)
