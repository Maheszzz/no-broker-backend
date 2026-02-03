#!/bin/bash

# Test Endpoints Script for no-broker-backend
# This script tests all API endpoints with curl commands

BASE_URL="http://localhost:8000"
API_PREFIX="/api/v1"

echo "=================================="
echo "  Testing no-broker-backend APIs"
echo "=================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test an endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo -e "${YELLOW}Testing: ${description}${NC}"
    echo "  Method: $method"
    echo "  Endpoint: $endpoint"
    
    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ $http_code -ge 200 ] && [ $http_code -lt 300 ]; then
        echo -e "  ${GREEN}✓ Status: $http_code${NC}"
    elif [ $http_code -ge 400 ] && [ $http_code -lt 500 ]; then
        echo -e "  ${YELLOW}⚠ Status: $http_code (Client Error)${NC}"
    else
        echo -e "  ${RED}✗ Status: $http_code (Error)${NC}"
    fi
    
    echo "  Response: $body"
    echo ""
    
    # Return the response for further use
    echo "$body"
}

# HEALTH CHECK ENDPOINTS
echo "=== HEALTH CHECK ENDPOINTS ==="
echo ""
test_endpoint "GET" "/" "Health check (root)" > /dev/null
test_endpoint "GET" "/health" "" "Health check (detailed)" > /dev/null

# CONTACT ENDPOINTS
echo "=== CONTACT ENDPOINTS ==="
echo ""

# List contacts
test_endpoint "GET" "${API_PREFIX}/realty/contacts" "" "List all contacts" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/contacts?skip=0&limit=10" "" "List contacts with pagination" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/contacts?status=new" "" "List contacts filtered by status" > /dev/null

# Create contact
echo "Creating a test contact..."
contact_data='{
  "name": "Test User",
  "phone": "9876543210",
  "email": "test@example.com",
  "message": "This is a test contact message",
  "status": "new"
}'
create_response=$(test_endpoint "POST" "${API_PREFIX}/realty/contacts" "$contact_data" "Create new contact")
contact_id=$(echo "$create_response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ ! -z "$contact_id" ]; then
    echo "Contact created with ID: $contact_id"
    
    # Get specific contact
    test_endpoint "GET" "${API_PREFIX}/realty/contacts/${contact_id}" "" "Get contact by ID" > /dev/null
    
    # Update contact
    update_data='{
      "status": "contacted",
      "message": "Updated test message"
    }'
    test_endpoint "PUT" "${API_PREFIX}/realty/contacts/${contact_id}" "$update_data" "Update contact" > /dev/null
    
    # Delete contact
    test_endpoint "DELETE" "${API_PREFIX}/realty/contacts/${contact_id}" "" "Delete contact" > /dev/null
fi

# Test invalid contact ID
test_endpoint "GET" "${API_PREFIX}/realty/contacts/99999" "" "Get non-existent contact" > /dev/null

# PROPERTY ENDPOINTS
echo "=== PROPERTY ENDPOINTS ==="
echo ""

# List properties
test_endpoint "GET" "${API_PREFIX}/realty/properties" "" "List all properties" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/properties?skip=0&limit=10" "" "List properties with pagination" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/properties?property_type=1BHK" "" "List properties filtered by type" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/properties?listing_type=rent" "" "List properties filtered by listing type" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/properties?is_available=true" "" "List available properties" > /dev/null

# Create property
echo "Creating a test property..."
property_data='{
  "property_name": "Test Property",
  "location": "Test Location",
  "property_type": "1BHK",
  "listing_type": "rent",
  "price": 15000,
  "deposit": 30000,
  "sqft": 850,
  "bedrooms": 1,
  "bathrooms": 1,
  "description": "This is a test property",
  "is_available": true
}'
create_prop_response=$(test_endpoint "POST" "${API_PREFIX}/realty/properties" "$property_data" "Create new property")
property_id=$(echo "$create_prop_response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ ! -z "$property_id" ]; then
    echo "Property created with ID: $property_id"
    
    # Get specific property
    test_endpoint "GET" "${API_PREFIX}/realty/properties/${property_id}" "" "Get property by ID" > /dev/null
    
    # Update property
    update_prop_data='{
      "price": 16000,
      "is_available": false
    }'
    test_endpoint "PUT" "${API_PREFIX}/realty/properties/${property_id}" "$update_prop_data" "Update property" > /dev/null
    
    # PROPERTY IMAGE ENDPOINTS
    echo "=== PROPERTY IMAGE ENDPOINTS ==="
    echo ""
    
    # List images for property
    test_endpoint "GET" "${API_PREFIX}/realty/properties/${property_id}/images" "" "List property images" > /dev/null
    
    # Add image to property
    image_data='{
      "image_url": "https://example.com/test-image.jpg",
      "is_primary": true,
      "sort_order": 1
    }'
    create_img_response=$(test_endpoint "POST" "${API_PREFIX}/realty/properties/${property_id}/images" "$image_data" "Add property image")
    image_id=$(echo "$create_img_response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    
    if [ ! -z "$image_id" ]; then
        echo "Image created with ID: $image_id"
        
        # Update image
        update_img_data='{
          "is_primary": false,
          "sort_order": 2
        }'
        test_endpoint "PUT" "${API_PREFIX}/realty/images/${image_id}" "$update_img_data" "Update property image" > /dev/null
        
        # Delete image
        test_endpoint "DELETE" "${API_PREFIX}/realty/images/${image_id}" "" "Delete property image" > /dev/null
    fi
    
    # Delete property
    test_endpoint "DELETE" "${API_PREFIX}/realty/properties/${property_id}" "" "Delete property" > /dev/null
fi

# Test invalid property ID
test_endpoint "GET" "${API_PREFIX}/realty/properties/99999" "" "Get non-existent property" > /dev/null

# Test metrics endpoint
echo "=== MONITORING ENDPOINTS ==="
echo ""
test_endpoint "GET" "/metrics" "" "Get Prometheus metrics" > /dev/null

echo "=================================="
echo "  Testing Complete!"
echo "=================================="
