import io
import json
import time
from typing import Any, Dict
from functools import partial

from flask import Blueprint, Response, request
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet


api = Blueprint("api", __name__)


@api.route("/health")
def health() -> str:
    return "OK"

@api.route("/print_numbers", methods=["POST"])
def print_numbers() -> Response:
    """Prints submitted numbers as a PDF"""
    if not request.is_json:
        return Response(
            json.dumps(
                {"error": f"JSON input expected; received '{request.mimetype}'"}
            ),
            status=406,
            mimetype="application/json",
        )

    params: Dict[str, Any] = request.get_json()  # type: ignore
    numbers = params.get("numbers", [])
    rows = [[str(idx + 1), num] for idx, num in enumerate(numbers)]

    styles = getSampleStyleSheet()
    title = Paragraph("Here are the numbers you have submitted:", styles["h2"])
    table = Table(data=rows)

    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(filename=buffer)
    pdf.build([title, table])

    buffer.seek(0)
    return Response(
        buffer,
        mimetype="application/pdf",
        headers={'Content-Disposition': f'attachment; filename=numbers{round(time.time())}.pdf'}
    )
