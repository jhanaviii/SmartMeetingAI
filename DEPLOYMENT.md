# SmartMeetingAI - Production Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying SmartMeetingAI to production.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- OpenAI API key

## Quick Production Setup

### 1. Clone and Setup

```bash
git clone <repository-url>
cd SmartMeetingAI
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with your production settings:

```env
# Flask Application Configuration
SECRET_KEY=your-production-secret-key-here
DATABASE_URL=sqlite:///smartmeeting.db

# OpenAI Configuration (Required)
OPENAI_API_KEY=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

# Application Settings
FLASK_ENV=production
FLASK_DEBUG=False
```

### 3. Initialize Database

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 4. Start Production Server

#### Option A: Using Gunicorn (Recommended)

```bash
gunicorn -c gunicorn.conf.py app:app
```

#### Option B: Using the production script

```bash
python run.py
```

#### Option C: Using Flask directly

```bash
export FLASK_ENV=production
python app.py
```

## Production Configuration

### Gunicorn Configuration

The `gunicorn.conf.py` file is pre-configured for production with:

- Multiple worker processes
- Proper logging
- Timeout settings
- Process management

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Flask secret key | Yes | Generated |
| `DATABASE_URL` | Database connection string | No | SQLite |
| `OPENAI_API_KEY` | OpenAI API key | Yes | None |
| `FLASK_ENV` | Environment mode | No | production |
| `FLASK_DEBUG` | Debug mode | No | False |

## Security Considerations

1. **Secret Key**: Use a strong, unique secret key in production
2. **API Keys**: Keep your OpenAI API key secure and never commit it to version control
3. **Database**: Consider using a production database like PostgreSQL for better performance
4. **HTTPS**: Use HTTPS in production with proper SSL certificates
5. **Firewall**: Configure firewall rules to restrict access

## Monitoring and Logging

### Health Check

The application provides a health check endpoint:

```bash
curl http://your-domain:5001/api/health
```

### Logs

Gunicorn logs are configured to output to stdout/stderr. For production, consider:

- Using a log aggregation service
- Implementing structured logging
- Setting up log rotation

## Scaling

### Horizontal Scaling

To scale horizontally:

1. Use a load balancer (nginx, HAProxy)
2. Run multiple Gunicorn instances
3. Use a shared database
4. Implement session storage (Redis)

### Vertical Scaling

To scale vertically:

1. Increase worker processes in `gunicorn.conf.py`
2. Use a more powerful server
3. Optimize database queries
4. Implement caching

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `gunicorn.conf.py`
2. **Database errors**: Ensure database file is writable
3. **OpenAI API errors**: Check API key and rate limits
4. **Memory issues**: Reduce worker processes

### Debug Mode

For debugging, temporarily enable debug mode:

```bash
export FLASK_DEBUG=True
export FLASK_ENV=development
python app.py
```

## Backup and Recovery

### Database Backup

```bash
# Backup SQLite database
cp instance/smartmeeting.db backup/smartmeeting_$(date +%Y%m%d_%H%M%S).db
```

### Application Backup

```bash
# Backup application files
tar -czf smartmeeting_backup_$(date +%Y%m%d_%H%M%S).tar.gz . --exclude=venv --exclude=__pycache__
```

## Performance Optimization

1. **Database**: Use connection pooling
2. **Caching**: Implement Redis caching
3. **Static Files**: Serve static files through nginx
4. **CDN**: Use a CDN for static assets
5. **Compression**: Enable gzip compression

## Support

For deployment issues:

1. Check the logs for error messages
2. Verify all environment variables are set
3. Test the health endpoint
4. Review the troubleshooting section above

## License

This deployment guide is part of the SmartMeetingAI project and follows the same license terms. 