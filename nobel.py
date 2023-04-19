from flask import Flask, render_template, request
import rdflib
g = rdflib.Graph()
result = g.parse("nobeldata.owl")
print("graph has %s statements." % len(g))
app = Flask(__name__)
#apis
#list_nations-GET: Return sorted names of all nations

#list_years-GET: Return sorted years nobels are awarded


#GET: Return sorted names of all nations
#list_nations api
@app.route('/nobel/nations')
def list_nations():
    qres = g.query(
            """
            PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
            SELECT ?nation
            {
                    ?g rdf:type table:PersonWinner;
                    table:nationality ?nation.
                    }
            GROUP BY ?nation
            ORDER BY ?nation""")

    nation = []
    for row in qres:
        print(row)
        name = str(row.nation).split('/')[-1]
        nation.append(name)
    return nation


#GET: Return sorted names of all nobel categories
@app.route('/nobel/categories')
def sorted_names_categories():
    qureyresult = g.query(
            """
            PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
            SELECT ?wonprice
            {
                    ?g rdf:type table:PersonWinner;
                    table:WonPrize ?wonprice.
                    }
            GROUP BY ?wonprice
            ORDER BY ?wonprice""")

    unique_categories = set()
    for row in qureyresult:
        category = str(row.wonprice).split('/')[-4]
        unique_categories.add(category)
    
    return sorted(list(unique_categories))


#GET: Return sorted years nobels are awarded
@app.route('/nobel/years')
def list_years():
    qureyresult = g.query(
            """
            PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
            SELECT ?wonprice
            {
                    ?g rdf:type table:PersonWinner;
                    table:WonPrize ?wonprice.
                    }
            GROUP BY ?wonprice
            ORDER BY ?wonprice""")

    unique_year = set()

    for row in qureyresult:
        year = str(row.wonprice).split('/')[-2]
        unique_year.add(year)
    
    return sorted(list(unique_year))


def list_winner_year():
#GET: Return list of all nobel winners for the given year
    year = 1902

    qres = g.query(
        """
        PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        SELECT ?name
        {
        ?g rdf:type table:PersonWinner;
        table:name ?name;
        table:WonPrize ?wonprice.
        ?wonprice table:yearWon ?year.
        FILTER (?year = """ + str(year) + """)
        }""")

    winners = []
    for row in qres:
        #print(row)
        name = str(row.name)
        winners.append(name)
    return winners

#GET: Return list of all nobel winners for the given nation
def list_winner_nation():
    nation = 'Argentina'

    qres = g.query(
        """
        PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        SELECT ?name ?nationality
        {
            ?g rdf:type table:PersonWinner;
            table:name ?name;
            table:nationality ?nationality.
        }""")


    winners = []
    for row in qres:
        if nation in row[1].split('/')[-1]:
            winner_name = row[0] + " " + row[1]
            winner_name = winner_name.split("http", 1)[0]
            winners.append(winner_name)

    return winners


def list_winner_category():
#GET: Return list of all nobel winners for the given category
    category = 'chemistry'
    qres = g.query(
        """
        PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        SELECT ?name ?wonprice
        {
            ?g rdf:type table:PersonWinner;
            table:name ?name;
            table:WonPrize ?wonprice.
        }
        GROUP BY ?wonprice
        ORDER BY ?wonprice""")


    winners = []
    for row in qres:
        if category in row[1].split('/')[-4]:
            winner_name = row[0] + " " + row[1]
            winner_name = winner_name.split("http", 1)[0]
            winners.append(winner_name)
    #print(len(winners))
    return winners


#GET: Return list of all nobel winners for the given year and category
def list_winner_year_category():
    category = 'chemistry'
    year = '1901'
    qres = g.query(
        """
        PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        SELECT ?name ?wonprice
        {
            ?g rdf:type table:PersonWinner;
            table:name ?name;
            table:WonPrize ?wonprice.
        }
        GROUP BY ?wonprice
        ORDER BY ?wonprice""")

    winners = []
    for row in qres:
        if category in str(row[1].split('/')[-4]) and year in str(row[1].split('/')[-2]):
            winner_name = row[0] + " " + row[1]
            winner_name = winner_name.split("http", 1)[0]
            winners.append(winner_name)
    return winners

