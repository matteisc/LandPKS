## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu
## 6/24/2015

library(shiny)
source('helpers.R')



shinyUI(pageWithSidebar(
  # Title of the application
  headerPanel("Plot user data"),
  
  sidebarPanel(
    tabsetPanel(id = "tabPanel1",
      tabPanel("Select user",
               br(),
               actionButton("selectAll", "Select All"),
               actionButton("deselectAll", "Deselect All"),
               uiOutput("UserList") ),

    tabPanel("Select date",
             br(),
             actionButton("selectAllMonth", "Select All"),
             actionButton("deselectAllMonth", "Deselect All"),
             uiOutput("MonthList"))
    ) ,width = 2),
  
  mainPanel(
    br(),
    htmlOutput ("chart1")
  )
))
