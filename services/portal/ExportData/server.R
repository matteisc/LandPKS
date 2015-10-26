## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

# server.R
source('helpers.R')
library(googleVis)

shinyServer(function(input, output,session) {
  

  output$url<- renderUI({
    
    link =paste0("https://landpotential.shinyapps.io/LandCoverCharts/?userName=",selectedRecorder())  
    a("Data Visualization", class = "btn btn-primary btn-md", href = link,
      target="_blank",
      style = "background-color:white ; color: black; border-color: #CDCDCD")
  })
    
 
  
getFilename <- function() { 
    if(input$dataType == "LandInfo"){
      paste('Export_LandInfo_Data', '.csv', sep='') 
    }
    else if(input$dataType == "LandCover")
    {
      paste('Export_LandCover_Data', '.csv', sep='') 
    }
    else if(input$dataType == "Metadata for LandInfo" )
    {
      paste('Export_METADATA_LandInfo', '.csv', sep='') 
    }
    else if(input$dataType == "Metadata for LandCover" )
    {
      paste('Export_METADATA_LandCover', '.csv', sep='') 
    }
    else
      "dummy.csv"
  }
  

  output$downloadData <- downloadHandler(  
    filename = getFilename(),
    content = function(file) { 
      req_data <- updateRequestedData(selectedRecorder(),isolate(input$dataType))
      req_data$recName <- NULL
      write.csv(req_data, file,row.names=FALSE,quote=TRUE,na="",qmethod='escape')
    }
  )
  
  isValidEmail <- function(x) {
    result = grepl("\\<[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}\\>", as.character(x), ignore.case=TRUE)
    return (result)
  }
  
   

selectedRecorder <- reactive({   
     rec <-""   
    if(input$exportAll)
    {
      rec = "all"
    }
    else
    {
      shiny::validate(need(input$recorder!= "", 'Please enter an email address!' ))
      shiny::validate(need(isValidEmail(input$recorder), 'Please enter a valid email address!' ))     
      rec <- input$recorder 
    } 
    rec  
  })
})

