## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

library(shiny)
source('helpers.R')


shinyUI(fluidPage(
  h3("Request Data Export"),
  
  
  
  conditionalPanel(
    condition = "input.exportAll == false",
    textInput("recorder", label = "Enter your recorder name :")
  ),
  
  
  
  checkboxInput("exportAll", label = h6("Export ALL plots in the database (download may take several minutes)"), value = FALSE),
  selectInput("dataType", label = h5("Type of Data Export"), 
              choices = list("LandInfo" , "LandCover" , "Methadata for LandInfo" , "Methadata for LandCover" ), 
              selected = "LandInfo"),
  
  downloadButton('downloadData', 'Export')
))

