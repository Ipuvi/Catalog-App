# Importing Flask...
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databasetup import Base, Category, Restaurant, MenuItem, Hotel, HotelDetails, Destination, DestinationDetails