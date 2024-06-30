from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import timezone, geocoder, carrier, PhoneNumberType, phonenumberutil

app = Flask(__name__)

@app.route('/track', methods=['GET'])
def track():
    number = request.args.get('number')
    if not number:
        return jsonify({"error": "No phone number provided"}), 400
    
    try:
        phone = phonenumbers.parse(f"+{number}")

        # Basic details
        time_zones = timezone.time_zones_for_number(phone)
        car = carrier.name_for_number(phone, "en")
        reg = geocoder.description_for_number(phone, "en")
        number_type = phonenumberutil.number_type(phone)

        # Additional details
        is_valid = phonenumberutil.is_valid_number(phone)
        is_possible = phonenumberutil.is_possible_number(phone)
        international_format = phonenumberutil.format_number(phone, phonenumberutil.PhoneNumberFormat.INTERNATIONAL)
        national_format = phonenumberutil.format_number(phone, phonenumberutil.PhoneNumberFormat.NATIONAL)
        e164_format = phonenumberutil.format_number(phone, phonenumberutil.PhoneNumberFormat.E164)
        country_code = phone.country_code
        region_code = phonenumberutil.region_code_for_country_code(country_code)
        location_description = geocoder.description_for_number(phone, "en")

        type_dict = {
            PhoneNumberType.FIXED_LINE: "FIXED_LINE",
            PhoneNumberType.MOBILE: "MOBILE",
            PhoneNumberType.FIXED_LINE_OR_MOBILE: "FIXED_LINE_OR_MOBILE",
            PhoneNumberType.TOLL_FREE: "TOLL_FREE",
            PhoneNumberType.PREMIUM_RATE: "PREMIUM_RATE",
            PhoneNumberType.SHARED_COST: "SHARED_COST",
            PhoneNumberType.VOIP: "VOIP",
            PhoneNumberType.PERSONAL_NUMBER: "PERSONAL_NUMBER",
            PhoneNumberType.PAGER: "PAGER",
            PhoneNumberType.UAN: "UAN",
            PhoneNumberType.VOICEMAIL: "VOICEMAIL",
            PhoneNumberType.UNKNOWN: "UNKNOWN"
        }

        response = {
            "phone": str(phone),
            "time_zones": list(time_zones),
            "carrier": car,
            "region": reg,
            "number_type": type_dict[number_type],
            "is_valid": is_valid,
            "is_possible_number": is_possible,
            "international_format": international_format,
            "national_format": national_format,
            "e164_format": e164_format,
            "country_code": country_code,
            "region_code": region_code,
            "location_description": location_description,
        }

        return jsonify(response)
    
    except phonenumbers.phonenumberutil.NumberParseException:
        return jsonify({"error": "Invalid phone number provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
