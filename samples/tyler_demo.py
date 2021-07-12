import difflib

from finpandas import fundamentals

form = fundamentals.ten_k("msft", [2019, 2018])
# print(form.search("Revenue"))

# print(form[2019])
def smart_search(query:str, form):
    matches = form.search(query)
    if len(matches) > 1:
        db = matches[2019]
        tags = []
        for i, row in db.iteritems():
            tags.append(i[0])
        match = difflib.get_close_matches(query, tags, 1, 0.2)[0]
        match = "^" + match + "$"
    elif len(matches) == 0:
        db = form[2019]
        tags = []
        for i, row in db.iteritems():
            tags.append(i[0])
        match = difflib.get_close_matches(query, tags, 1, 0.2)[0]
        match = "^" + match + "$"
    else:
        match = query

    return form.search(match)

print(smart_search("SellingGeneralAndAdministrativeExpense", form))
