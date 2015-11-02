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
      

  output$downloadData <- downloadHandler(  
    filename = function(){
      if(input$dataType == "LandInfo"){
              'Export_LandInfo_Data.csv' 
            }
            else if(input$dataType == "LandCover")
            {
              'Export_LandCover_Data.csv' 
            }
            else if(input$dataType == "Metadata for LandInfo" )
            {
              'Export_METADATA_LandInfo.csv'
            }
            else if(input$dataType == "Metadata for LandCover" )
            {
              'Export_METADATA_LandCover.csv'
            }
            else
              "dummy.csv"
        
    },
    content = function(file) { 
      req_data <- updateRequestedData(selectedRecorder(),isolate(input$dataType))
      if(is.null(req_data) || nrow(req_data) == 0 ){
        stop("No data to display!")
      }
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

