import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the Yale Economics Department Placement Dashboard - 2021", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        
        dbc.Row([
            dbc.Col(html.H5(children='This Dashboard enables the comparison of PhD placements of different Universities in the United States. The universities included in this analysis are: Yale, Harvard, MIT, NYU, UPenn, Stanford, Northwestern, Princeton, University of Minnesota, UChicago, Columbia, UC Berkeley, Brown, Duke, Boston University, UCLA, Michigan and Cornell' )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='The Placements of candidates have been grouped into the following categories:')
                    , className="mb-5")
        ]),
        
        dbc.Row([
            dbc.Col(html.H5(children='Academia_1: Tier 1 Departments of Economics: Harvard, M.I.T., Princeton, Stanford, Berkeley, Yale, Northwestern, Chicago, Columbia, Penn, LSE, UCL, Cambridge, Oxford. Tier 1 Finance Groups at Business Schools: Harvard, Wharton, Booth, Sloan, Kellogg, Stanford, Haas, Tuck, Columbia, Yale')
                    , className="mb-5")
        ]),
        
        dbc.Row([
            dbc.Col(html.H5(children='Academia_2: Tier 2 Departments of Economics: NYU, UCLA, UC San Diego, Michigan, Wisconsin, Cornell, Duke, Minnesota, Brown, CMU, Maryland, BU, Johns Hopkins, Boston College, Penn State, Toulouse, Bocconi, Australian National University. Tier 2 Finance Groups at Business Schools: Michigan, Duke, NYU, Virginia, UCLA, Cornell, Texas at Austin, University of North Carolina, CMU, Emory, Georgetown, Indiana, Washington University in St. Louis, USC, Arizona State, Vanderbilt')
            , className="mb-5")
        ]),

        dbc.Row([
            dbc.Col(html.H5(children='Academia_3: Tier 3: all other research universities, excluding professional schools (except business) and liberal arts colleges')
            , className="mb-5")
        ]),
        
        dbc.Row([
            dbc.Col(html.H5(children='Professional Schools: All Professional Schools not in the Tier 1 and 2 Finance Groups at Business Schools')
            , className="mb-5")
            ]),
                    
        dbc.Row([
            dbc.Col(html.H5(children='Central Banks: Central Bank Institutions in different countries including Multi-lateral Development Banks such as World Bank')
            , className="mb-5")
            ]),
                    
        dbc.Row([
            dbc.Col(html.H5(children='Other Govt Jobs: Departments of State-owned entities and related organizations')
            , className="mb-5")
        ]),
                    
        dbc.Row([
            dbc.Col(html.H5(children='Econ Consulting: Top Tier Consulting Organizations as well as Economic Consulting Groups')
            , className="mb-5")
        ]),
                    
        dbc.Row([
            dbc.Col(html.H5(children='Private Sector Banks: All private sector banks including financial asset management institutions')
            , className="mb-5")
        ]),
            
        dbc.Row([
            dbc.Col(html.H5(children='Non-ladder Academic: Academic positions not associated with Tenure Track at Academic Institutions')
            , className="mb-5")
        ]),
            
        dbc.Row([
            dbc.Col(html.H5(children='Postdoc: Post-Doctoral Programs')
            , className="mb-5")
        ]),
            
        dbc.Row([
            dbc.Col(html.H5(children='Non-profit: Non-profit or research organizations')
            , className="mb-5")
        ]),
            
        dbc.Row([
            dbc.Col(html.H5(children='Others: Private sector companies or organizations that do not fall in any of the above categories')
            , className="mb-5")
        ]),
            
        dbc.Row([
            dbc.Col(html.H5(children='Econ_Acad: Sum of Academia_1, Academia_2 and Academia_3')
            , className="mb-5")
        ]),
            
        dbc.Row([
            dbc.Col(html.H5(children='All_Academia: Sum of Academia_1, Academia_2, Academia_3 and Professional Schools')
            , className="mb-5")
        ]),
                   
        dbc.Row([
            dbc.Col(html.H5(children='All_Private: Sum of Private Sector Banks and Others')
            , className="mb-5")
        ]),
                   
            
        dbc.Row([
            dbc.Col(html.H5(children='Private Sector Banks: All private sector banks including financial asset management institutions')
            , className="mb-5")
        ]),                             
    ]),
])



# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)