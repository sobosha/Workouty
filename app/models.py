from sqlalchemy import Float, String, Integer, Column, DateTime, ForeignKey, func ,Text , CheckConstraint
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column,relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
class Exercises(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    muscle_group: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
class WorkoutPlans(Base):
    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    plan_exercises: Mapped[list["WorkoutPlanExercises"]] = relationship("WorkoutPlanExercises", back_populates="workout_plan", cascade="all, delete-orphan")
    
class WorkoutPlanExercises(Base):
    __tablename__ = "workout_plan_exercises"
    __table_args__ = (
    CheckConstraint('sets_target > 0', name='check_sets_target_positive'),
    CheckConstraint('(reps_target IS NULL OR reps_target > 0)', name='check_reps_target_positive'),
    CheckConstraint('(durration_target_seconds IS NULL OR durration_target_seconds > 0)', name='check_durration_target_seconds_non_negative'),
    CheckConstraint('(weight IS NULL OR weight >= 0)', name='check_weight_non_negative'),
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workout_plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("workout_plans.id"), nullable=False)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets_target: Mapped[int] = mapped_column(Integer, nullable=False)
    reps_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    durration_target_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    workout_plan: Mapped["WorkoutPlans"] = relationship("WorkoutPlans", back_populates="plan_exercises")