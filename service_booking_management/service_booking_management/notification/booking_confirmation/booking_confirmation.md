<p>Hi {{ doc.customer_name }},</p>

<p>Your service booking has been confirmed. Please find the attached booking receipt.</p>

<ul>
  <li><strong>Booking ID:</strong> {{ doc.name }}</li>
  <li><strong>Service Type:</strong> {{ doc.service_type }}</li>
  <li><strong>Date & Time:</strong> {{ frappe.utils.format_datetime(doc.preferred_date_time) }}</li>
  <li><strong>Status:</strong> {{ doc.status }}</li>
</ul>

<p>Thank you for booking with us!</p>

<p>Regards,<br>
The Wellness Team</p>