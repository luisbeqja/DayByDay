#!/bin/bash
 
cd backend
source venv/bin/activate
hypercorn app:app --bind 0.0.0.0:5000 --reload 