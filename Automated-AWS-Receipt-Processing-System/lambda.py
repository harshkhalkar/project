import json
import os
import boto3
import uuid
from datetime import datetime
import urllib.parse

# Initialize AWS clients
s3 = boto3.client('s3')
textract = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

# Environment variables
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'Receipts')
SES_SENDER_EMAIL = os.environ.get('SES_SENDER_EMAIL', 'your-email@example.com')
SES_RECIPIENT_EMAIL = os.environ.get('SES_RECIPIENT_EMAIL', 'recipient@example.com')

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

        print(f"Processing receipt from {bucket}/{key}")

        # Verify object exists
        try:
            s3.head_object(Bucket=bucket, Key=key)
            print("Object verified successfully.")
        except Exception as e:
            raise Exception(f"Failed to verify object: {str(e)}")

        # Process receipt with Textract
        receipt_data = process_receipt_with_textract(bucket, key)

        # Store in DynamoDB
        store_receipt_in_dynamodb(receipt_data)

        # Send email notification
        send_email_notification(receipt_data)

        return {'statusCode': 200, 'body': json.dumps('Receipt processed successfully!')}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}


def process_receipt_with_textract(bucket, key):
    try:
        response = textract.analyze_expense(
            Document={'S3Object': {'Bucket': bucket, 'Name': key}}
        )
    except Exception as e:
        raise Exception(f"Textract analyze_expense failed: {str(e)}")

    receipt_id = str(uuid.uuid4())
    receipt_data = {
        'receipt_id': receipt_id,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'vendor': 'Unknown',
        'total': '0.00',
        'subtotal': '0.00',
        'tax': '0.00',
        'discount': '0.00',
        'invoice_number': 'N/A',
        'payment_method': 'N/A',
        'due_date': 'N/A',
        'billing_address': '',
        'shipping_address': '',
        'items': [],
        's3_path': f"s3://{bucket}/{key}"
    }

    if 'ExpenseDocuments' in response and response['ExpenseDocuments']:
        doc = response['ExpenseDocuments'][0]
        for field in doc.get('SummaryFields', []):
            field_type = field.get('Type', {}).get('Text') or field.get('LabelDetection', {}).get('Text', '')
            value = field.get('ValueDetection', {}).get('Text', '')
            confidence = field.get('ValueDetection', {}).get('Confidence', 0)

            if confidence < 80:
                continue

            mappings = {
                'TOTAL': 'total',
                'SUBTOTAL': 'subtotal',
                'TAX': 'tax',
                'DISCOUNT': 'discount',
                'VENDOR_NAME': 'vendor',
                'INVOICE_RECEIPT_DATE': 'date',
                'INVOICE_RECEIPT_ID': 'invoice_number',
                'PAYMENT_METHOD': 'payment_method',
                'DUE_DATE': 'due_date',
                'BILLING_ADDRESS': 'billing_address',
                'SHIPPING_ADDRESS': 'shipping_address',
            }

            if field_type in mappings:
                receipt_data[mappings[field_type]] = value

        for group in doc.get('LineItemGroups', []):
            for line_item in group.get('LineItems', []):
                item = {}
                for field in line_item.get('LineItemExpenseFields', []):
                    field_type = field.get('Type', {}).get('Text', '')
                    value = field.get('ValueDetection', {}).get('Text', '')
                    confidence = field.get('ValueDetection', {}).get('Confidence', 0)

                    if confidence < 80:
                        continue

                    if field_type == 'ITEM':
                        item['name'] = value
                    elif field_type == 'DESCRIPTION':
                        item['description'] = value
                    elif field_type == 'PRICE':
                        item['price'] = value
                    elif field_type == 'UNIT_PRICE':
                        item['unit_price'] = value
                    elif field_type == 'QUANTITY':
                        item['quantity'] = value
                    elif field_type == 'PRODUCT_CODE':
                        item['product_code'] = value

                if 'name' in item:
                    receipt_data['items'].append(item)

    print(f"Extracted receipt data: {json.dumps(receipt_data)}")
    return receipt_data


def store_receipt_in_dynamodb(receipt_data):
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        items = [{
            'name': i.get('name', ''),
            'description': i.get('description', ''),
            'price': i.get('price', '0.00'),
            'unit_price': i.get('unit_price', ''),
            'quantity': i.get('quantity', '1'),
            'product_code': i.get('product_code', '')
        } for i in receipt_data['items']]

        db_item = {
            'receipt_id': receipt_data['receipt_id'],
            'date': receipt_data['date'],
            'vendor': receipt_data['vendor'],
            'invoice_number': receipt_data['invoice_number'],
            'total': receipt_data['total'],
            'subtotal': receipt_data['subtotal'],
            'tax': receipt_data['tax'],
            'discount': receipt_data['discount'],
            'payment_method': receipt_data['payment_method'],
            'due_date': receipt_data['due_date'],
            'billing_address': receipt_data['billing_address'],
            'shipping_address': receipt_data['shipping_address'],
            'items': items,
            's3_path': receipt_data['s3_path'],
            'processed_timestamp': datetime.now().isoformat()
        }

        table.put_item(Item=db_item)
        print(f"Stored in DynamoDB: {receipt_data['receipt_id']}")
    except Exception as e:
        raise Exception(f"Error storing in DynamoDB: {str(e)}")


def send_email_notification(receipt_data):
    try:
        items_html = ""
        for i in receipt_data['items']:
            items_html += f"<li>{i.get('name', 'Unknown')} - ${i.get('price', 'N/A')} x {i.get('quantity', '1')}</li>"
        if not items_html:
            items_html = "<li>No items found</li>"

        html_body = f"""
        <html><body>
        <h2>Receipt Notification</h2>
        <p><strong>Receipt ID:</strong> {receipt_data['receipt_id']}</p>
        <p><strong>Vendor:</strong> {receipt_data['vendor']}</p>
        <p><strong>Date:</strong> {receipt_data['date']}</p>
        <p><strong>Total:</strong> ${receipt_data['total']}</p>
        <p><strong>Payment Method:</strong> {receipt_data['payment_method']}</p>
        <p><strong>Due Date:</strong> {receipt_data['due_date']}</p>
        <p><strong>Billing Address:</strong> {receipt_data['billing_address']}</p>
        <p><strong>Shipping Address:</strong> {receipt_data['shipping_address']}</p>
        <h3>Items:</h3><ul>{items_html}</ul>
        </body></html>
        """

        ses.send_email(
            Source=SES_SENDER_EMAIL,
            Destination={'ToAddresses': [SES_RECIPIENT_EMAIL]},
            Message={
                'Subject': {'Data': f"Receipt Processed: {receipt_data['vendor']}"},
                'Body': {'Html': {'Data': html_body}}
            }
        )
        print("Email sent.")
    except Exception as e:
        print(f"Email failed: {str(e)}")
        # Continue execution even if SES fails

