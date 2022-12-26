setwd('/Users/mamane/Desktop/UCL/Year 2/Term 1/STAT0006/ICA 3')
data <- read.csv('live_streams.csv')
transfor_mod <- function(model){
  #Clearing outliers
  model_fitted<-fitted(model)
  model_stdres<-rstandard(model)
  new_1 <- abs(model_stdres)
  outliers_pos <- as.vector(which(new_1>5))
  #clearing leverages
  hat_val <- hatvalues(model)
  leverages <- which(hat_val>((2*length(model$coefficients)/length(model$fitted.values))))
  unusual <- c(outliers, leverages)
  
  print(new_2)
  data <- data[-unusual,]
  model_fitted<-model_fitted[-unusual]
  model_stdres<-model_stdres[-unusual]
  
  #Checking linearity
  par(mfrow = c(2,2))
  plot(new$subscribers, model_stdres, main = 'Linearity', 
       ylab = 'Standardized residuals', xlab = 'Subscribers')
  abline(a = 0, b = 0, col = 'red', lty = 2)
  
  #Checking homoscedasticity and normality
  plot(model_fitted, model_stdres, xlab="Model Fitted", ylab="Standardised residuals",
       main = 'Homoscedasticity')
  abline(a=0, b = 0, col = 'red', lty = 2)
  
  qqnorm(model_stdres, ylab = "Standardized Residuals", xlab = "Quantiles of N(0,1)",
          main = 'Normality')
  qqline(model_stdres)
  plot(model_stdres, xlab = 'time', ylab = 'Standardized residuals',
       main = 'independency')
  
  print(summary(model))

  library(lmtest)
  print(dwtest(model, alternative = 'greater'))
}

model3_A <- lm(sqrt(viewers) ~ genre + host + subscribers + day + 
                 season + guests + ads_last +
                 subscribers*genre , data = data )

transfor_mod(model3_A)

a <- plot(model3_A)[1]

model3_A2 <- lm(sqrt(viewers) ~ genre + host + subscribers + day + 
                   guests + guests*genre + 
                  subscribers*genre , data = data )
summary(model3_A2)
sd_resid_2 <- rstandard(model3_A2)
fitted_2 <- fitted(model3_A2)






