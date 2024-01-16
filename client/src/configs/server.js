import dotenv from 'dotenv'
dotenv.config()

export const ServerConfig = {
    PATH: process.env.PATH || 'http://localhost:5000/api'
}