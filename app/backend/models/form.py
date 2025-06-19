import uuid

from database.database import Base
from sqlalchemy import JSON, Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Form(Base):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        String(36), unique=True, index=True, default=lambda: str(uuid.uuid4())
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(String, nullable=False)

    questions = relationship("Question", back_populates="form")


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    option_text = Column(String, nullable=False)
    option_value = Column(String, nullable=False)

    question = relationship("Question", back_populates="options")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("forms.id"), nullable=False)

    question_text = Column(String, nullable=True)
    question_type = Column(
        Enum(
            "short_text",
            "long_text",
            "radio",
            "checkbox",
            "signature",
            "picture",
            "table",
            name="question_types",
        ),
        nullable=False,
    )
    required = Column(Boolean, default=False)

    options = relationship("QuestionOption", back_populates="question")
    form = relationship("Form", back_populates="questions")
