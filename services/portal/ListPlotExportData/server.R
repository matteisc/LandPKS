## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

# server.R
source('helpers.R')
library(shiny)
library(googleVis)

shinyServer(function(input, output) {
  
  output$downloadData <- downloadHandler(
    filename = function() { paste('Export_LandInfo_Data', '.csv', sep='') },
    content = function(file) {
      write.csv(csv_data, file,row.names=FALSE,quote=TRUE,na="",qmethod='escape')
    }
  )
})