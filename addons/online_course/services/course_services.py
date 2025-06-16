# services/course_services.py
# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional, TYPE_CHECKING
from odoo import _
from odoo.exceptions import ValidationError  # ✅ Use built-in exception

if TYPE_CHECKING:
    from ..models.res_users import ResUsers
    from ..models.course import Course

from ..static.constants import CourseConstants
from ..validators.course_validators import EnrollmentValidator, PriceValidator
from ..services.notification_factory import NotificationFactory
# ❌ Remove this import:
# from ..exception.exceptions import EnrollmentError, CourseStateError


class CourseSecurityService:
    """Handles course security and permissions."""

    def __init__(self, env) -> None:
        self.env = env

    def can_edit_course_details(
        self, course: "Course", user: Optional["ResUsers"] = None
    ) -> bool:
        """Check if user can edit course details."""
        user = user or self.env.user
        return (
            user.has_group(CourseConstants.Security.ADMIN_GROUP)
            or course.teacher_id == user
        )

    def can_edit_price(
        self, course: "Course", user: Optional["ResUsers"] = None
    ) -> bool:
        """Check if user can edit course price."""
        return self.can_edit_course_details(course, user)

    def can_edit_teacher(
        self, course: "Course", user: Optional["ResUsers"] = None
    ) -> bool:
        """Check if user can change teacher assignment."""
        user = user or self.env.user
        return user.has_group(CourseConstants.Security.ADMIN_GROUP)


class CourseEnrollmentService:
    """Handles course enrollment operations."""

    def __init__(self, env) -> None:
        self.env = env
        self.validator = EnrollmentValidator()

    def enroll_student(self, course: "Course", student: "ResUsers") -> Dict[str, Any]:
        """Enroll a student in a course."""
        try:
            self.validator.validate(course, student)
        except Exception as e:
            # Convert any validator exception to ValidationError
            raise ValidationError(str(e))

        course.sudo().write({"student_ids": [(4, student.id)]})
        return NotificationFactory.create_enrollment_success(course.name)

    def unenroll_student(self, course: "Course", student: "ResUsers") -> Dict[str, Any]:
        """Unenroll a student from a course."""
        if student not in course.student_ids:
            # ✅ Use ValidationError instead of EnrollmentError
            raise ValidationError(_(CourseConstants.Messages.NOT_ENROLLED))

        course.sudo().write({"student_ids": [(3, student.id)]})
        return NotificationFactory.create_unenrollment_success(course.name)


class CourseStateService:
    """Handles course state transitions."""

    def __init__(self, env) -> None:
        self.env = env
        self.price_validator = PriceValidator()

    def publish_course(self, course: "Course") -> None:
        """Publish a course."""
        try:
            self.price_validator.validate(course)
        except Exception as e:
            # Convert any validator exception to ValidationError
            raise ValidationError(str(e))

        course.state = CourseConstants.States.PUBLISHED

    def close_enrollment(self, course: "Course") -> None:
        """Close course enrollment."""
        if course.state != CourseConstants.States.PUBLISHED:
            # ✅ Use ValidationError instead of CourseStateError
            raise ValidationError(_("Can only close enrollment for published courses."))
        course.state = CourseConstants.States.CLOSED

    def reopen_enrollment(self, course: "Course") -> None:
        """Reopen course enrollment."""
        if course.state != CourseConstants.States.CLOSED:
            # ✅ Use ValidationError instead of CourseStateError
            raise ValidationError(_("Can only reopen enrollment for closed courses."))
        course.state = CourseConstants.States.PUBLISHED

    def archive_course(self, course: "Course") -> None:
        """Archive a course."""
        course.state = CourseConstants.States.ARCHIVED

    def set_to_draft(self, course: "Course") -> None:
        """Set course back to draft."""
        if course.student_ids:
            # ✅ Use ValidationError instead of CourseStateError
            raise ValidationError(
                _("Cannot set course '%s' to draft because it has enrolled students.")
                % course.name
            )
        course.state = CourseConstants.States.DRAFT
