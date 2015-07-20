## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu
## 6/30/2015


# server.R
source('helpers.R')
library(shiny)
library(googleVis)


shinyServer(function(input, output,session) {

  
  output$UserList <- renderUI({  
    
    div(style='height:500px;  overflow: scroll'  
            ,checkboxGroupInput("checkGroup", 
                               label = h5("Usernames:"), 
                               choices = userNames ,
                               selected = userNames))      
  })
  
  observe({
    if (input$selectAll){
      
      updateCheckboxGroupInput( session, "checkGroup", 
                                choices = userNames ,
                                selected = userNames) 
    }
  })
  
  observe({
    if(input$deselectAll)
    {
      updateCheckboxGroupInput( session, "checkGroup", 
                                choices = userNames ,
                                selected = NULL  ) 
    }
    
  })
  

  ###########################

  output$chart1 <- renderGvis({
  
    shiny::validate(need(input$checkGroup , 'Check at least one userName!' ))    
    #shiny::validate(need(input$checkMonthGroup , 'Check at least one date!' )) 
    shiny::validate(need(input$dates[2] > input$dates[1], "end date should be after start date"))

    UserData<-getUserData(input$checkGroup,input$dates,input$count)
    
    shiny::validate(need(UserData , 'No data to display!' ))  

    
    gvisColumnChart(UserData)

  })
  
  
    output$stats <- renderText({
      paste(input$checkGroup,input$dates,input$count)
      
      paste("Plot Statistics (user/month): ", "",
            paste("Mean : ",statMean),
            paste("Median : ", statMedian),
            paste("min : ", statMin),
            paste("Max : ", statMax),sep="\n")
      })
  
}) 
