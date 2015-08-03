## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

library(shiny)
library(shinydashboard)
source('helpers.R')

dashboardPage(
  dashboardHeader(title ="LandInfo dashboard"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("User/Plot chart", tabName = "userPlot", icon = icon("bar-chart")),
      menuItem("Organization/Plot chart", tabName = "orgPlot", icon = icon("bar-chart"), badgeLabel = "new", badgeColor = "green"),
      menuItem("Data Table", tabName = "dataTable", icon = icon("table"), badgeLabel = "new", badgeColor = "green")
      
      )
    ),
  dashboardBody(
       tabItems(
                   tabItem("userPlot",
                           fluidRow(
                                 box(width = 12, height = 250, htmlOutput ("chart1"))                                 
                             ),
                           fluidRow(
                                 box(width = 3,tabsetPanel(id = "tabPanel1",
                                   tabPanel("Select user",
                                            br(),
                                            actionButton("selectAll", "Select All"),
                                            actionButton("deselectAll", "Deselect All"),
                                            uiOutput("UserList") ),
                             
                                 tabPanel("Select date",
                                          br(), 
                                          dateRangeInput("dates", label = h3("Date range"),
                                                         min = as.Date(minDate, "%Y-%m-%d") ,
                                                         max = as.Date(maxDate, "%Y-%m-%d"),
                                                         start = as.Date(minDate, "%Y-%m-%d"),
                                                         end = as.Date(maxDate, "%Y-%m-%d")),
                                          sliderInput("count", "Number of uploaded plots per user/month",
                                                      minCount, maxCount, c(minCount, maxCount), step = 1)
                                          )
                                 )
                                 ),
                                 box(width = 6,verbatimTextOutput("stats"))
                             )
                   ),
                   tabItem("orgPlot",
                           fluidRow(
                             box(width = 12, height = 250,htmlOutput ("chartOrg"))
                           ),
                           fluidRow(
                             box(width = 3,tabsetPanel(id = "tabPanelOrg1",
                                                       tabPanel("Select organization",
                                                                br(),
                                                                actionButton("selectAllOrg", "Select All"),
                                                                actionButton("deselectAllOrg", "Deselect All"),
                                                                uiOutput("OrgList") ),
                                                       
                                                       tabPanel("Select date",
                                                                br(), 
                                                                dateRangeInput("datesOrg", label = h3("Date range"),
                                                                               min = as.Date(minDate, "%Y-%m-%d") ,
                                                                               max = as.Date(maxDate, "%Y-%m-%d"),
                                                                               start = as.Date(minDate, "%Y-%m-%d"),
                                                                               end = as.Date(maxDate, "%Y-%m-%d")),
                                                                sliderInput("countOrg", "Number of uploaded plots per org/month",
                                                                            minOrgCount, maxOrgCount, c(minOrgCount, maxOrgCount), step = 1)
                                                       )
                             )
                             ),
                             box(width = 6,verbatimTextOutput("orgStats"))
                           )
                   ),
                   tabItem("dataTable",
                           div(style = 'overflow-x: scroll', dataTableOutput("tbl")))
                           
                 )
               )
)
