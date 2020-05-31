# JARR-disaster-relief
## How to use

### 1. Register: 
\[POST] localhost:5000/JARR-disaster-relief/signup
	Using a form with these keys:
  
      email
      password
      is_admin
      bank_account_number
      routing_number
      first_name
      last_name
      address
      city
      zip_code
  
- Register as a system administrator: set is_admin to true.
- By registering you are able to supply and request resources.

### 2. Add a request for a given resource: 
\[POST] localhost:5000/JARR-disaster-relief/requests
		Using a form or json with these keys:
    
      category_id (category of product, see list below)
      person_id (person who needs supply)
      name (name of supply)
      quantity
      description
      max_unit_price (max price willing to pay)
      address
      city
      zip_code
### 3. Announce the availability of a resource:
\[POST] localhost:5000/JARR-disaster-relief/supplies
    Using a form or json with these keys:
    
      category_id
      person_id
      name
      brand
      quantity
      description
      sunit_price (price per unit)
      address
      city
      zip_code

### 4. Reserve or purchase a resource. Free resources are reserved. Otherwise, they are purchased. (Reserve is purchasing something that’s free)
\[POST] localhost:5000/JARR-disaster-relief/purchase
		Using a form or json with these keys:
    
      supply_id (id of supply being purchased)
      person_id (id of person buying resource)
      pquantity (number of units to purchase)
      
### 4.5) Fulfill a request for a resource.
 \[POST] localhost:5000/JARR-disaster-relief/fulfill
		Using a form or json with these keys:
    
      request_id (id of request being fulfilled
      person_id (id of person supplying resource)
      fquantity (number of units)
      
### 5. Browse resources being requested 
\[GET] localhost:5000/JARR-disaster-relief/requests

### 6. Browse resources available 
\[GET] localhost:5000/JARR-disaster-relief/supplies

### 7. Keyword search resources being requested, with sorting by resource name 
(Same as 5, but) Using arguments for:

    max_unit_price
    category
    name (can match partially, but case-sensitive)
    
### 8. Keyword search resources available, with sorting by resource name
(Same as 6, but) Using (one or more) arguments such as:

    sunit_price
    category
    subcategory
    name (can match partially, but case-sensitive)
    brand

### The resource categories handled are:
	1. Water
		a. Small bottles
		b. 1 Gallon bottles
	2. Medications
	3. Baby Food
	4. Canned Food
	5. Dry Food
	6. Ice
	7. Fuel
		a. Diesel
		b. Propane
		c. Gasoline
	8. Medical Devices
	9. Heavy Equipment
	10. Tools
	11. Clothing
	12. Power Generators
	13. Batteries
