from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSON, JSONB, UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class JBBot(Base):
    __tablename__ = "jb_bot"

    id = Column(String, primary_key=True)  # "1234"
    name = Column(String)  # "My Bot"
    dsl = Column(String)
    code = Column(String)
    requirements = Column(String)
    index_urls = Column(ARRAY(String))
    status = Column(String, nullable=False, default="active")  # active or deleted
    timeout = Column(Integer, default=24*60*60)
    supported_languages = Column(ARRAY(String))
    config_env = Column(JSON)  # variables to pass to the bot environment
    required_credentials = Column(ARRAY(String))  # ["API_KEY", "API_SECRET"]
    credentials = Column(JSON)  # {"API_KEY and other secrets"}
    version = Column(String, nullable=False)  # 0.0.1
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
    )
    users = relationship("JBUser", back_populates="bot")
    sessions = relationship("JBSession", back_populates="bot")
    channels = relationship("JBChannel", back_populates="bot")


class JBChannel(Base):
    __tablename__ = "jb_channel"

    id = Column(String, primary_key=True)
    bot_id = Column(String, ForeignKey("jb_bot.id"))
    status = Column(String, nullable=False)  # active or inactive
    name = Column(String)
    type = Column(String)
    key = Column(String)
    app_id = Column(String)
    url = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    turns = relationship("JBTurn", back_populates="channel")
    sessions = relationship("JBSession", back_populates="channel")
    bot = relationship("JBBot", back_populates="channels")


class JBUser(Base):
    __tablename__ = "jb_users"

    id = Column(String, primary_key=True)
    bot_id = Column(String, ForeignKey("jb_bot.id"))
    first_name = Column(String)
    last_name = Column(String)
    identifier = Column(String)
    language_preference = Column(String, default="en")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    bot = relationship("JBBot", back_populates="users")
    turns = relationship("JBTurn", back_populates="user")


class JBTurn(Base):
    __tablename__ = "jb_turn"

    id = Column(String, primary_key=True)
    session_id = Column(String, ForeignKey("jb_session.id"))
    bot_id = Column(String, ForeignKey("jb_bot.id"))
    channel_id = Column(String, ForeignKey("jb_channel.id"))
    user_id = Column(String, ForeignKey("jb_users.id"))
    turn_type = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    session = relationship("JBSession", back_populates="turns")
    messages = relationship("JBMessage", back_populates="turn")
    channel = relationship("JBChannel", back_populates="turns")
    user = relationship("JBUser", back_populates="turns")


class JBMessage(Base):
    __tablename__ = "jb_message"

    id = Column(String, primary_key=True)
    turn_id = Column(String, ForeignKey("jb_turn.id"))
    message_type = Column(String)
    message = Column(JSON, nullable=False)
    is_user_sent = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    turn = relationship("JBTurn", back_populates="messages")


class JBDocumentStoreLog(Base):
    __tablename__ = "jb_document_store_log"

    uuid = Column(String, primary_key=True)
    bot_id = Column(String)  # , ForeignKey('jb_bot.id'))
    documents_list = Column(ARRAY(Text))
    total_file_size = Column(Float)
    status_code = Column(Integer)
    status_message = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class JBQALog(Base):
    __tablename__ = "jb_qa_log"

    id = Column(String, primary_key=True)
    pid = Column(String)  # , ForeignKey('jb_users.id'))
    # You should define jb_bot model
    bot_id = Column(String)  # , ForeignKey('jb_bot.id'))
    # , ForeignKey('jb_document_store_log.uuid'))
    document_uuid = Column(String)
    input_language = Column(String, default="en")
    query = Column(String)
    audio_input_link = Column(String)
    response = Column(String)
    audio_output_link = Column(String)
    retrieval_k_value = Column(Integer)
    retrieved_chunks = Column(ARRAY(Text))
    prompt = Column(String)
    gpt_model_name = Column(String)
    status_code = Column(Integer)
    status_message = Column(String)
    response_time = Column(Integer)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class JBSTTLog(Base):
    __tablename__ = "jb_stt_log"

    id = Column(String, primary_key=True)
    qa_log_id = Column(String)  # , ForeignKey('jb_qa_log.id'))
    audio_input_bytes = Column(String)
    model_name = Column(String)
    text = Column(String)
    status_code = Column(Integer)
    status_message = Column(String)
    response_time = Column(Integer)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class JBTTSLog(Base):
    __tablename__ = "jb_tts_log"

    id = Column(String, primary_key=True)
    qa_log_id = Column(String)  # , ForeignKey('jb_qa_log.id'))
    text = Column(String)
    model_name = Column(String)
    audio_output_bytes = Column(String)
    status_code = Column(Integer)
    status_message = Column(String)
    response_time = Column(Integer)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class JBTranslatorLog(Base):
    __tablename__ = "jb_translator_log"

    id = Column(String, primary_key=True)
    qa_log_id = Column(String)  # , ForeignKey('jb_qa_log.id'))
    text = Column(String)
    input_language = Column(String)
    output_language = Column(String)
    model_name = Column(String)
    translated_text = Column(String)
    status_code = Column(Integer)
    status_message = Column(String)
    response_time = Column(Integer)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class JBChatHistory(Base):
    __tablename__ = "jb_chat_history"

    id = Column(String, primary_key=True)
    pid = Column(String)  # , ForeignKey('jb_users.id'))
    # You should define jb_bot model
    bot_id = Column(String)  # , ForeignKey('jb_bot.id'))
    # , ForeignKey('jb_document_store_log.uuid'))
    document_uuid = Column(String)
    message_owner = Column(String, nullable=False)
    preferred_language = Column(String, nullable=False)
    audio_url = Column(String)
    message = Column(String)
    message_in_english = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class JBSession(Base):
    __tablename__ = "jb_session"

    id = Column(String, primary_key=True)
    bot_id = Column(String, ForeignKey("jb_bot.id"))
    channel_id = Column(String, ForeignKey("jb_channel.id"))
    variables = Column(JSON)
    
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
    )
    bot = relationship("JBBot", back_populates="sessions")
    channel = relationship("JBChannel", back_populates="sessions")
    turns = relationship("JBTurn", back_populates="session")


class JBPluginUUID(Base):
    __tablename__ = "jb_plugin_uuid"

    id = Column(String, primary_key=True)
    session_id = Column(String)
    turn_id = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
    )


class JBForm(Base):
    __tablename__ = "jb_form"

    id = Column(String, primary_key=True)
    bot_id = Column(String, ForeignKey("jb_bot.id"))
    parameters = Column(JSON)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
    )


# class LangchainPgCollection(Base):
#     __tablename__ = 'langchain_pg_collection'

#     name = Column(String, nullable=True)
#     cmetadata = Column(JSON(astext_type=Text()), nullable=True)
#     uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)


# class LangchainPgEmbedding(Base):
#     __tablename__ = 'langchain_pg_embedding'

#     collection_id = Column(UUID(as_uuid=True), ForeignKey('langchain_pg_collection.uuid', ondelete='CASCADE'), nullable=True)
#     embedding = Column(JSONB, nullable=True)
#     document = Column(String, nullable=True)
#     cmetadata = Column(JSON(astext_type=Text()), nullable=True)
#     custom_id = Column(String, nullable=True)
#     uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
#     collection = relationship('LangchainPgCollection', back_populates='embeddings')
