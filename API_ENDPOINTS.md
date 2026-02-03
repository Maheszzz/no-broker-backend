# API Endpoints Documentation

## Base URL
```
http://localhost:8000
```

## Health Check Endpoints

### 1. Root Health Check
```bash
curl http://localhost:8000/
```
**Response:**
```json
{"status":"healthy","service":"Realty API"}
```

### 2. Detailed Health Check
```bash
curl http://localhost:8000/health
```
**Response:**
```json
{"status":"healthy","service":"Realty API","version":"1.0.0"}
```

---

## Contact Endpoints

### 1. List All Contacts
```bash
# Basic listing
curl http://localhost:8000/api/v1/realty/contacts

# With pagination
curl "http://localhost:8000/api/v1/realty/contacts?skip=0&limit=10"

# Filter by status
curl "http://localhost:8000/api/v1/realty/contacts?status=new"
# Available statuses: new, contacted, closed
```

### 2. Get Contact by ID
```bash
curl http://localhost:8000/api/v1/realty/contacts/1
```

### 3. Create Contact
```bash
curl -X POST http://localhost:8000/api/v1/realty/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "9876543210",
    "email": "john@example.com",
    "message": "I am interested in your property",
    "status": "new"
  }'
```
**Required Fields:**
- `name`: 1-100 characters
- `phone`: 10-15 characters
- `email`: Valid email format
- `message`: Max 250 characters
- `status`: Optional (new, contacted, closed) - defaults to "new"

### 4. Update Contact
```bash
curl -X PUT http://localhost:8000/api/v1/realty/contacts/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "contacted",
    "message": "Follow-up scheduled for next week"
  }'
```
**Note:** All fields are optional. Only provided fields will be updated.

### 5. Delete Contact
```bash
curl -X DELETE http://localhost:8000/api/v1/realty/contacts/1
```

---

## Property Endpoints

### 1. List All Properties
```bash
# Basic listing
curl http://localhost:8000/api/v1/realty/properties

# With pagination
curl "http://localhost:8000/api/v1/realty/properties?skip=0&limit=10"

# Filter by property type
curl "http://localhost:8000/api/v1/realty/properties?property_type=1BHK"
# Available types: PG, 1RK, 1BHK, 2BHK

# Filter by listing type
curl "http://localhost:8000/api/v1/realty/properties?listing_type=rent"
# Available types: buy, rent

# Filter by availability
curl "http://localhost:8000/api/v1/realty/properties?is_available=true"

# Combine filters
curl "http://localhost:8000/api/v1/realty/properties?property_type=PG&listing_type=rent&is_available=true&limit=5"
```

### 2. Get Property by ID
```bash
curl http://localhost:8000/api/v1/realty/properties/1
```
**Note:** This also returns all associated images.

### 3. Create Property
```bash
# PG Property Example
curl -X POST http://localhost:8000/api/v1/realty/properties \
  -H "Content-Type: application/json" \
  -d '{
    "property_name": "Cozy PG in Koramangala",
    "location": "Koramangala, Bangalore",
    "phone": "9876543210",
    "map_link": "https://maps.google.com/example",
    "description": "Fully furnished PG with WiFi, TV, and food",
    "property_type": "PG",
    "furnishing": "fully_furnished",
    "single_price": 8000,
    "double_price": 6000,
    "triple_price": 5000,
    "listing_type": "rent",
    "is_available": true
  }'

# 1BHK/2BHK Property Example
curl -X POST http://localhost:8000/api/v1/realty/properties \
  -H "Content-Type: application/json" \
  -d '{
    "property_name": "Modern 2BHK Apartment",
    "location": "Whitefield, Bangalore",
    "phone": "9876543210",
    "map_link": "https://maps.google.com/example",
    "description": "Spacious 2BHK with parking",
    "property_type": "2BHK",
    "furnishing": "semi_furnished",
    "private_price": 25000,
    "listing_type": "rent",
    "is_available": true
  }'
```

**Required Fields:**
- `property_name`: 1-150 characters
- `location`: 1-150 characters
- `phone`: 10-15 characters (REQUIRED)
- `property_type`: PG, 1RK, 1BHK, or 2BHK

**Optional Fields:**
- `map_link`: Valid URL (http:// or https://)
- `description`: Text
- `furnishing`: fully_furnished, semi_furnished, unfurnished (default: unfurnished)
- `private_price`: For 1RK, 1BHK, 2BHK
- `single_price`: For PG single occupancy
- `double_price`: For PG double occupancy
- `triple_price`: For PG triple occupancy
- `listing_type`: buy or rent (default: rent)
- `is_available`: true or false (default: true)

### 4. Update Property
```bash
curl -X PUT http://localhost:8000/api/v1/realty/properties/1 \
  -H "Content-Type: application/json" \
  -d '{
    "single_price": 8500,
    "is_available": false,
    "description": "Updated description"
  }'
```
**Note:** All fields are optional. Only provided fields will be updated.

### 5. Delete Property
```bash
curl -X DELETE http://localhost:8000/api/v1/realty/properties/1
```
**Note:** This will also delete all associated images (CASCADE delete).

---

## Property Image Endpoints

### 1. List Property Images
```bash
curl http://localhost:8000/api/v1/realty/properties/1/images
```

### 2. Add Property Image
```bash
curl -X POST http://localhost:8000/api/v1/realty/properties/1/images \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/property-image.jpg",
    "is_primary": true,
    "sort_order": 1
  }'
```
**Required Fields:**
- `image_url`: Valid URL (max 500 characters)

**Optional Fields:**
- `is_primary`: true/false (default: false) - Marks the main property image
- `sort_order`: Integer >= 0 (default: 0) - Display order

### 3. Update Property Image
```bash
curl -X PUT http://localhost:8000/api/v1/realty/images/1 \
  -H "Content-Type: application/json" \
  -d '{
    "is_primary": false,
    "sort_order": 2
  }'
```
**Note:** All fields are optional.

### 4. Delete Property Image
```bash
curl -X DELETE http://localhost:8000/api/v1/realty/images/1
```

---

## Monitoring Endpoints

### Prometheus Metrics
```bash
curl http://localhost:8000/metrics
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": {
    "error": "not_found",
    "message": "Contact with id 999 not found"
  }
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "phone"],
      "msg": "String should have at least 10 characters",
      "input": "123"
    }
  ]
}
```

### 500 Database Error
```json
{
  "detail": {
    "error": "database_error",
    "message": "Failed to create property: ..."
  }
}
```

---

## Query Parameters

### Pagination (Available on list endpoints)
- `skip`: Number of records to skip (default: 0, min: 0)
- `limit`: Maximum records to return (default: 100, min: 1, max: 100)

Example:
```bash
curl "http://localhost:8000/api/v1/realty/properties?skip=10&limit=5"
```

### Filters

**Contacts:**
- `status`: new, contacted, closed

**Properties:**
- `property_type`: PG, 1RK, 1BHK, 2BHK
- `listing_type`: buy, rent
- `is_available`: true, false

---

## Status Codes

- **200** - Success (GET, PUT)
- **201** - Created (POST)
- **204** - No Content (DELETE)
- **404** - Not Found
- **422** - Validation Error
- **500** - Server Error

---

## Notes

1. **Phone Field**: The `phone` field is REQUIRED when creating a property. This is enforced by the database.

2. **Images**: When you delete a property, all associated images are automatically deleted.

3. **Validation**: All fields are validated according to their constraints (length, format, etc.)

4. **CORS**: The API allows requests from `http://localhost:3000` by default.

5. **Rate Limiting**: Rate limiting is enabled on all endpoints.

---

## Testing

Run the comprehensive test suite:
```bash
./test_all_endpoints.sh
```

This will test all endpoints and report success/failure for each one.
