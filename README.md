
![Logo](https://github.com/Pranshu1902/JobPulse-fe/assets/70687348/3e0f3433-9f76-4485-bfaa-40d2e16369d3)


# JobPulse

JobPulse simplifies your job application process by keeping all your applications organized in one place. Track your progress and manage deadlines, ensuring you never miss an opportunity. With an intuitive interface and easy-to-use features, JobPulse helps you stay on top of your job search with ease.



[![Deployment](https://img.shields.io/badge/Railway-Success-green.svg)](https://choosealicense.com/licenses/mit/)

[![Production](https://img.shields.io/badge/API-Released-green.svg)](https://opensource.org/licenses/)

## Features

- Kanban Board view of Applications
- Timeline view of Application Status
- Add Comments for each application
- Easy filtering on Job Applications


## Tech Stack

**Client:** Next.Js, TailwindCSS

**Server:** Django, Django Rest Framework

**Database:** PostgreSQL


## Run Backend Locally

Clone the project

```bash
  git clone git@github.com:Pranshu1902/JobPulse.git
```

Go to the project directory

```bash
  cd JobPulse
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Migrate Tables to Database

```bash
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```


## Environment Variables
To run this project, you will need to add the following environment variables to your `.env` file.

`SECRET_KEY`

`DEBUG`

`DATABASE_URL`
## API Reference

Documentation: https://jobpulse.up.railway.app/docs/

## Deployment

Production: https://jobpulse-fe.vercel.app/

Frontend Repository: https://github.com/Pranshu1902/JobPulse-fe
## Screenshots

Backend Deployment:
![Backend Deployment](https://github.com/Pranshu1902/JobPulse/assets/70687348/e3097a28-bf9c-40dc-af08-a34f64b46229)

API Swagger UI Documentation:
![API Swagger UI Documentation](https://github.com/Pranshu1902/JobPulse/assets/70687348/a27439b6-3cf9-440e-ac07-6304df55d9be)
