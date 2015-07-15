## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu
## 6/30/2015

library(shiny)

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
             dateRangeInput("dates", label = h3("Date range"),
                            min = as.Date(minDate, "%Y-%m-%d") ,
                            max = as.Date(maxDate, "%Y-%m-%d"),
                            start = as.Date(minDate, "%Y-%m-%d"),
                            end = as.Date(maxDate, "%Y-%m-%d")),
             sliderInput("count", "Number of uploaded plots per user/month",
                         minCount, maxCount, c(minCount, maxCount), step = 1)
             
             )
    ) ,width = 2),
  
  mainPanel(
    br(),
    htmlOutput ("chart1"),
    br(),
    br(),
    verbatimTextOutput("stats")
  )
))
