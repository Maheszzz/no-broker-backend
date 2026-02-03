#!/bin/bash

# Comprehensive API Test Script
# Tests all endpoints and reports results

BASE_URL="http://localhost:8000"
API_PREFIX="/api/v1"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

echo "=================================="
echo "  API Endpoint Testing Suite"
echo "=================================="
echo ""

test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    local expected_code=$5
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" 2>&1)
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" 2>&1)
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" == "$expected_code" ]; then
        echo -e "${GREEN}✓ PASS${NC} | $description"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAIL${NC} | $description"
        echo -e "  Expected: $expected_code, Got: $http_code"
        if [ ! -z "$body" ]; then
            echo -e "  Response: ${body:0:200}"
        fi
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    
    # Return response body for further use
    echo "$body"
}

echo -e "${BLUE}=== HEALTH CHECK ENDPOINTS ===${NC}"
test_endpoint "GET" "/" "" "Root health check" "200" > /dev/null
test_endpoint "GET" "/health" "" "Detailed health check" "200" > /dev/null
echo ""

echo -e "${BLUE}=== CONTACT ENDPOINTS ===${NC}"
test_endpoint "GET" "${API_PREFIX}/realty/contacts" "" "List all contacts" "200" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/contacts?skip=0&limit=10" "" "List contacts with pagination" "200" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/contacts?status=new" "" "List contacts by status filter" "200" > /dev/null

# Create contact
contact_data='{
  "name": "John Doe",
  "phone": "9876543210",
  "email": "john@example.com",
  "message": "I am interested in your property"
}'
create_response=$(test_endpoint "POST" "${API_PREFIX}/realty/contacts" "$contact_data" "Create contact" "201")
contact_id=$(echo "$create_response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ ! -z "$contact_id" ]; then
    test_endpoint "GET" "${API_PREFIX}/realty/contacts/${contact_id}" "" "Get contact by ID" "200" > /dev/null
    
    update_contact='{
      "status": "contacted"
    }'
    test_endpoint "PUT" "${API_PREFIX}/realty/contacts/${contact_id}" "$update_contact" "Update contact" "200" > /dev/null
    test_endpoint "DELETE" "${API_PREFIX}/realty/contacts/${contact_id}" "" "Delete contact" "204" > /dev/null
fi

# Test error cases
test_endpoint "GET" "${API_PREFIX}/realty/contacts/99999" "" "Get non-existent contact (404)" "404" > /dev/null

# Test invalid contact creation
invalid_contact='{
  "name": "",
  "phone": "123",
  "email": "invalid-email"
}'
test_endpoint "POST" "${API_PREFIX}/realty/contacts" "$invalid_contact" "Create invalid contact (422)" "422" > /dev/null

echo ""

echo -e "${BLUE}=== PROPERTY ENDPOINTS ===${NC}"
test_endpoint "GET" "${API_PREFIX}/realty/properties" "" "List all properties" "200" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/properties?skip=0&limit=5" "" "List properties with pagination" "200" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/properties?property_type=PG" "" "Filter by property type" "200" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/properties?listing_type=rent" "" "Filter by listing type" "200" > /dev/null
test_endpoint "GET" "${API_PREFIX}/realty/properties?is_available=true" "" "Filter by availability" "200" > /dev/null

# Create property
property_data='{
  "property_name": "Luxury PG Accommodation",
  "location": "Koramangala, Bangalore",
  "phone": "9876543210",
  "map_link": "https://maps.google.com/test",
  "description": "Fully furnished PG with all amenities",
  "property_type": "PG",
  "furnishing": "fully_furnished",
  "single_price": 8000,
  "double_price": 6000,
  "triple_price": 5000,
  "listing_type": "rent",
  "is_available": true
}'
create_prop_response=$(test_endpoint "POST" "${API_PREFIX}/realty/properties" "$property_data" "Create property" "201")
property_id=$(echo "$create_prop_response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ ! -z "$property_id" ]; then
    test_endpoint "GET" "${API_PREFIX}/realty/properties/${property_id}" "" "Get property by ID" "200" > /dev/null
    
    update_property='{
      "single_price": 8500,
      "is_available": false
    }'
    test_endpoint "PUT" "${API_PREFIX}/realty/properties/${property_id}" "$update_property" "Update property" "200" > /dev/null
    
    echo ""
    echo -e "${BLUE}=== PROPERTY IMAGE ENDPOINTS ===${NC}"
    test_endpoint "GET" "${API_PREFIX}/realty/properties/${property_id}/images" "" "List property images" "200" > /dev/null
    
    # Add image
    image_data='{
      "image_url": "https://example.com/property-main.jpg",
      "is_primary": true,
      "sort_order": 1
    }'
    create_img_response=$(test_endpoint "POST" "${API_PREFIX}/realty/properties/${property_id}/images" "$image_data" "Add property image" "201")
    image_id=$(echo "$create_img_response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    
    if [ ! -z "$image_id" ]; then
        update_image='{
          "sort_order": 2,
          "is_primary": false
        }'
        test_endpoint "PUT" "${API_PREFIX}/realty/images/${image_id}" "$update_image" "Update property image" "200" > /dev/null
        test_endpoint "DELETE" "${API_PREFIX}/realty/images/${image_id}" "" "Delete property image" "204" > /dev/null
    fi
    
    # Test error cases for images
    test_endpoint "GET" "${API_PREFIX}/realty/properties/99999/images" "" "Get images for non-existent property (404)" "404" > /dev/null
    test_endpoint "PUT" "${API_PREFIX}/realty/images/99999" '{"sort_order": 1}' "Update non-existent image (404)" "404" > /dev/null
    
    # Clean up: delete property
    test_endpoint "DELETE" "${API_PREFIX}/realty/properties/${property_id}" "" "Delete property" "204" > /dev/null
fi

# Test error cases for properties
test_endpoint "GET" "${API_PREFIX}/realty/properties/99999" "" "Get non-existent property (404)" "404" > /dev/null

# Test invalid property creation (missing required fields)
invalid_property='{
  "property_name": "Test",
  "location": "Test Location"
}'
test_endpoint "POST" "${API_PREFIX}/realty/properties" "$invalid_property" "Create invalid property (422)" "422" > /dev/null

echo ""
echo -e "${BLUE}=== MONITORING ENDPOINTS ===${NC}"
test_endpoint "GET" "/metrics" "" "Prometheus metrics endpoint" "200" > /dev/null

echo ""
echo "=================================="
echo "  Test Results Summary"
echo "=================================="
echo -e "Total Tests:  ${BLUE}${TOTAL_TESTS}${NC}"
echo -e "Passed:       ${GREEN}${PASSED_TESTS}${NC}"
echo -e "Failed:       ${RED}${FAILED_TESTS}${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Please review the errors above.${NC}"
    exit 1
fi
