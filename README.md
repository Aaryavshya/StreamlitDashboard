# IoT Device Pipeline

## Overview

The IoT device pipeline demonstrates the flow of the data from the end effector that is the variable resistance sensor to the web application
that is hosted on the streamlit platform and GitHub.

## The Pipeline

End Effector Circuitry -> Arduino -> laptop server -> firebase -> laptop server -> streamlit web application -> Android WebApp Wrapper

firebase -> Google Drive -> ML Model -> Google Drive -> laptop server -> firebase -> laptop server -> streamlit web application -> Android
WebApp Wrapper.

This is a long pipeline with branching flow and the optimizations are to be done on the level of the laptop server, as we are the host and the client both for different devices I believe.