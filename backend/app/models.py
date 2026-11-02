# models.py - every class here becomes one table in the database.
# Each Column becomes a column of that table.

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


# ---------- Location tables (to support all-India reporting) ----------

class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    cities = relationship("City", back_populates="state")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)

    state = relationship("State", back_populates="cities")


# ---------- Users ----------
# role is one of: "citizen", "collector", "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(15))
    password_hash = Column(String(255), nullable=False)  # never store plain passwords
    role = Column(String(20), nullable=False, default="citizen")
    city_id = Column(Integer, ForeignKey("cities.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    city = relationship("City")


# ---------- Reports ----------
# status goes: pending -> verified -> assigned -> collected -> closed
# (or "rejected" if the admin rejects it)

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    citizen_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    description = Column(Text)
    photo_path = Column(String(255), nullable=False)   # we save the photo on disk, only the path here
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    pincode = Column(String(6))

    ai_category = Column(String(30))      # what the AI predicted
    final_category = Column(String(30))   # what the citizen finally chose
    status = Column(String(20), nullable=False, default="pending")
    reject_reason = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    citizen = relationship("User")
    city = relationship("City")


# ---------- Assignments (admin gives a report to a collector) ----------

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    collector_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    proof_photo_path = Column(String(255))

    report = relationship("Report")
    collector = relationship("User")


# ---------- Points (a ledger: every change in points is one row) ----------
# points can be positive (earned) or negative (spent on a reward)
# is_verified = False means "pending", True means "can be redeemed"

class PointTransaction(Base):
    __tablename__ = "point_transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_id = Column(Integer, ForeignKey("reports.id"))
    points = Column(Integer, nullable=False)
    reason = Column(String(100), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


# ---------- Rewards ----------

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    points_cost = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)


class Redemption(Base):
    __tablename__ = "redemptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reward_id = Column(Integer, ForeignKey("rewards.id"), nullable=False)
    status = Column(String(20), nullable=False, default="requested")  # requested/approved/rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    reward = relationship("Reward")
