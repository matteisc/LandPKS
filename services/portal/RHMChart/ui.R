library(shiny)
source('helpers.R')

shinyUI(pageWithSidebar(
  # Title of the application
  headerPanel("LandCover Data"),
  
  sidebarPanel(
    h4("Select chart:"),
    selectInput("charts", "", 
                choices = c("Cover/Bare ground chart" ,
                            "Height class multi bar chart",
                            "Gap percentage chart",
                            "Species Density chart",
                            "Plant Cover/Composition multi bar chart",
                            "Foliar Cover chart",
                            "test combined chart"
                            ),
                selected = "Cover/Bare ground chart"),
    
    h4("Select plot: "),
    #checkboxInput ('checkAll', 'Select All',value = NULL),
    actionButton("selectAll", "Select All"),
    actionButton("deselectAll", "Deselect All"),
    uiOutput("PlotNames")),
  
  mainPanel(
  br(),
  htmlOutput ("chart1"),
  h4("Description"),
  textOutput("summary")
)
))

