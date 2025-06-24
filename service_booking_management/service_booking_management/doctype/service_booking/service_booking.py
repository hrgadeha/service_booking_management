# Copyright (c) 2025, Hardik Gadesha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.integrations.utils import make_post_request


class ServiceBooking(Document):
	def after_insert(self):
		send_booking_data(self.name)
	
	def on_update(self):
		if self.status == "Approved" and self.email_sent == False:
			self.send_approval_email()
	
	def send_approval_email(self):
		try:
			subject = f"Your Service Booking is Confirmed - {self.name}"

			message = f"""
			<p>Hi { self.customer_name },</p>

			<p>Your service booking has been confirmed. Please find the attached booking receipt.</p>

			<ul>
				<li><strong>Booking ID:</strong> { self.name }</li>
				<li><strong>Service Type:</strong> { self.service_type }</li>
				<li><strong>Date & Time:</strong> { frappe.utils.format_datetime(self.preferred_date_time) }</li>
				<li><strong>Status:</strong> { self.status }</li>
			</ul>

			<p>Thank you for booking with us!</p>

			<p>Regards,<br>
			The Wellness Team</p>
			"""

			frappe.sendmail(
				recipients=[self.customer_email],
				subject=subject,
				message=message
			)

			self.db_set("email_sent", True)
			frappe.db.commit()

		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "send_approval_email Error")


@frappe.whitelist(allow_guest=False)
def send_booking_data(booking_id):
	if not booking_id:
		return {
			"http_status_code": 400,
			"status": "error",
			"message": "Booking ID is a mandatory parameter."
		}

	if booking_id and not frappe.db.exists("Service Booking", booking_id):
		return {
			"http_status_code": 400,
			"status": "error",
			"message": f"Booking ID {booking_id} not found"
		}

	service_booking_doc = frappe.get_doc("Service Booking", booking_id)
		
	url = "https://webhook.site/d20767e9-e393-4051-9e9e-99651fe90c6d"

	payload = {
		"id": service_booking_doc.name,
		"customer": service_booking_doc.customer,
		"customer_name": service_booking_doc.customer_name,
		"service_type": service_booking_doc.service_type,
		"preferred_time": str(service_booking_doc.preferred_date_time),
		"status": service_booking_doc.status
	}

	try:
		response = make_post_request(url, data=payload)

		return {
			"http_status_code": response.status_code if hasattr(response, 'status_code') else 200,
			"status": "success",
			"message": "Webhook sent successfully",
			"data_sent": payload
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "send_booking_data Webhook Error")

		return {
			"http_status_code": 400,
			"status": "error",
			"message": "Failed to send booking data to the webhook."
		}