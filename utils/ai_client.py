"""Wrapper unificato per le API AI (Anthropic Claude e OpenAI GPT)."""

import streamlit as st

_anthropic_client = None
_openai_client = None


def _get_anthropic():
    global _anthropic_client
    if _anthropic_client is None:
        import anthropic
        _anthropic_client = anthropic.Anthropic(
            api_key=st.secrets["ANTHROPIC_API_KEY"]
        )
    return _anthropic_client


def _get_openai():
    global _openai_client
    if _openai_client is None:
        import openai
        _openai_client = openai.OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
        )
    return _openai_client


def chat(
    system_prompt: str,
    messages: list[dict],
    provider: str | None = None,
    max_tokens: int = 1024,
) -> str:
    """Invia una conversazione all'AI e ritorna la risposta testuale.

    Args:
        system_prompt: Il system prompt da usare.
        messages: Lista di {"role": "user"|"assistant", "content": "..."}.
        provider: "anthropic" o "openai". Se None, usa il default da secrets.
        max_tokens: Massimo numero di token nella risposta.

    Returns:
        La risposta dell'AI come stringa.
    """
    if provider is None:
        provider = st.secrets.get("AI_PROVIDER", "anthropic")

    if provider == "anthropic":
        return _chat_anthropic(system_prompt, messages, max_tokens)
    else:
        return _chat_openai(system_prompt, messages, max_tokens)


def _chat_anthropic(system_prompt: str, messages: list[dict], max_tokens: int) -> str:
    client = _get_anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text


def _chat_openai(system_prompt: str, messages: list[dict], max_tokens: int) -> str:
    client = _get_openai()
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=max_tokens,
        messages=full_messages,
    )
    return response.choices[0].message.content


def chat_stream(
    system_prompt: str,
    messages: list[dict],
    provider: str | None = None,
    max_tokens: int = 1024,
):
    """Versione streaming: ritorna un generatore di chunk di testo.

    Usare con st.write_stream() per mostrare la risposta in tempo reale.
    """
    if provider is None:
        provider = st.secrets.get("AI_PROVIDER", "anthropic")

    if provider == "anthropic":
        yield from _stream_anthropic(system_prompt, messages, max_tokens)
    else:
        yield from _stream_openai(system_prompt, messages, max_tokens)


def _stream_anthropic(system_prompt: str, messages: list[dict], max_tokens: int):
    client = _get_anthropic()
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


def _stream_openai(system_prompt: str, messages: list[dict], max_tokens: int):
    client = _get_openai()
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    stream = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=max_tokens,
        messages=full_messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
