pies= []

pies.append({"id":1, "filling":'cherry', "price":12.99, "quantity":2})
pies.append({"id":2, "filling":'apple', "price":13.99, "quantity":2})
pies.append({"id":3, "filling":'berry', "price":14.99, "quantity":4})

test_me = {"id":4, "filling":'apple', "price":12.49, "quantity":3}

if not any(pie['filling'] == test_me["filling"] for pie in pies):
    pies.append(test_me)
    print(pies)
    
else:
    for pie in pies:
        if pie["filling"] == test_me["filling"]:
            pie["quantity"] += test_me["quantity"]
            print(pie)
            break