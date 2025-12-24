# 🛡️ NRC System Admin Operations Guide
## Comprehensive Administrator Manual

---

## 🎯 Administrator Overview

### Role & Responsibilities
As an NRC System Administrator, you are responsible for:
- **Application Processing**: Review and approve/reject NRC applications
- **User Management**: Manage user accounts and permissions
- **System Monitoring**: Ensure system performance and security
- **Report Generation**: Create analytics and compliance reports
- **Data Integrity**: Maintain accurate and secure data
- **Support**: Assist users with technical issues

### Admin Privileges
- **OTP Bypass**: Direct login without email verification
- **Full System Access**: All features and data
- **User Account Control**: Create, modify, disable accounts
- **Application Override**: Approve/reject with admin notes
- **System Configuration**: Modify settings and parameters
- **Report Access**: Generate all types of reports

---

## 🔐 Admin Login & Security

### Secure Login Process
1. **Direct Access**: Admins bypass OTP for efficiency
2. **Strong Authentication**: Use complex passwords
3. **Session Management**: Automatic logout after inactivity
4. **Access Logging**: All admin actions are logged

### Security Best Practices
- **Password Policy**: Minimum 12 characters, mixed case, numbers, symbols
- **Regular Updates**: Change passwords every 90 days
- **Secure Networks**: Only access from trusted networks
- **Two-Person Rule**: Critical actions require verification
- **Audit Trail**: Review access logs regularly

---

## 📋 Application Management

### Application Review Process

#### 1. Pending Applications Queue
**Access**: Dashboard → Applications → Pending Review

**Priority Order**:
1. **Urgent**: Replacement for lost/stolen NRC
2. **Standard**: New applications by submission date
3. **Follow-up**: Applications requiring additional information

#### 2. Application Review Steps

**Step 1: Initial Assessment**
- Verify applicant identity
- Check for duplicate applications
- Confirm eligibility (age, citizenship)

**Step 2: Document Verification**
- **Birth Certificate**: Verify authenticity and details
- **Proof of Residence**: Confirm current address
- **Photos**: Check quality and compliance
- **Signatures**: Verify digital signature

**Step 3: Data Validation**
- Cross-reference with existing records
- Verify address and constituency details
- Check for any red flags or inconsistencies

**Step 4: Decision Making**
- **Approve**: Generate NRC number and approve
- **Reject**: Provide detailed reason
- **Request Info**: Ask for additional documents

#### 3. Approval Process

**For Approval**:
1. Click **"Approve Application"**
2. System generates unique NRC number
3. Add admin notes (optional)
4. Confirm approval
5. Applicant receives email notification

**NRC Number Format**: `XXXXXX/XX/X`
- First 6 digits: Sequential number
- Next 2 digits: Year of issue
- Last digit: Check digit

#### 4. Rejection Process

**For Rejection**:
1. Click **"Reject Application"**
2. **Select Reason**:
   - Insufficient documentation
   - Invalid documents
   - Duplicate application
   - Eligibility issues
   - Other (specify)
3. **Add Detailed Notes**: Explain what needs correction
4. **Provide Guidance**: How applicant can reapply
5. Confirm rejection
6. Applicant receives detailed email

#### 5. Request Additional Information

**When More Info Needed**:
1. Click **"Request Additional Information"**
2. **Specify Requirements**:
   - Which documents needed
   - Quality improvements required
   - Additional verification needed
3. **Set Deadline**: Usually 30 days
4. **Send Request**: Applicant receives email with requirements

---

## 👥 User Management

### User Account Administration

#### 1. View All Users
**Access**: Dashboard → Users → All Users

**User Information Displayed**:
- Username and full name
- Email and phone number
- Registration date
- Last login
- Account status (Active/Inactive)
- Number of applications

#### 2. User Account Actions

**Activate/Deactivate Account**:
- Temporarily disable problematic accounts
- Reactivate after issues resolved
- Maintain audit trail of actions

**Reset Password**:
- Generate temporary password
- Force password change on next login
- Send secure notification to user

**Modify User Details**:
- Update contact information
- Correct name spelling errors
- Update address information

#### 3. Create Admin Accounts

**New Admin Creation**:
1. Navigate to Users → Create Admin
2. **Required Information**:
   - Username (unique)
   - Email address
   - Full name
   - Initial password
   - Permission level
3. **Permission Levels**:
   - **Super Admin**: Full system access
   - **Application Officer**: Application processing only
   - **Report Viewer**: Read-only access to reports
   - **Support Staff**: User assistance only

---

## 📊 Reporting & Analytics

### Report Types Available

#### 1. Summary Reports
**Purpose**: High-level system overview
**Includes**:
- Total applications by status
- Processing time averages
- Geographic distribution
- Demographic breakdowns
- Performance metrics

**Generation**:
1. Dashboard → Reports → Summary Report
2. Select date range
3. Choose export format (PDF, Excel, Word, CSV)
4. Generate and download

#### 2. Detailed Reports
**Purpose**: Comprehensive application listings
**Includes**:
- Complete application details
- User information
- Processing timeline
- Document status
- Admin actions

**Filters Available**:
- Date range
- Application status
- Geographic location
- Application type
- Processing officer

#### 3. Exception Reports
**Purpose**: Identify problematic applications
**Includes**:
- Long pending applications (>30 days)
- Missing documentation
- Duplicate applications
- Rejected applications without notes
- System errors

**Priority Levels**:
- **Critical**: Immediate attention required
- **High**: Address within 24 hours
- **Medium**: Address within week

#### 4. Performance Reports
**Purpose**: System efficiency analysis
**Includes**:
- Processing time trends
- Officer productivity
- Application volume patterns
- System usage statistics
- Error rates

### Report Scheduling
**Automated Reports**:
- Daily: Exception reports to supervisors
- Weekly: Summary reports to management
- Monthly: Comprehensive analytics
- Quarterly: Performance reviews

---

## ⚙️ System Administration

### System Configuration

#### 1. Email Settings
**SMTP Configuration**:
- Server: smtp.gmail.com
- Port: 587
- Security: TLS
- Authentication: App passwords

**Email Templates**:
- OTP verification emails
- Application status notifications
- Password reset emails
- Admin alerts

#### 2. Security Settings
**Authentication**:
- OTP expiry time (default: 10 minutes)
- Password complexity requirements
- Session timeout (default: 30 minutes)
- Failed login attempt limits

**Access Control**:
- IP address restrictions
- Admin permission levels
- Audit logging settings
- Data retention policies

#### 3. Application Settings
**Processing Parameters**:
- Auto-approval criteria (if any)
- Document size limits
- Supported file formats
- Application form fields

**NRC Generation**:
- Number sequence management
- Check digit algorithm
- Duplicate prevention
- Archive procedures

### Database Management

#### 1. Backup Procedures
**Daily Backups**:
- Automated at 2:00 AM
- Stored locally and cloud
- Retention: 30 days local, 1 year cloud
- Verification of backup integrity

**Manual Backup**:
```bash
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

#### 2. Data Maintenance
**Regular Tasks**:
- Clean temporary files
- Archive old applications
- Update user statistics
- Optimize database indexes

**Monthly Tasks**:
- Full database optimization
- Security audit
- Performance review
- Capacity planning

---

## 🚨 Emergency Procedures

### System Outages

#### 1. Immediate Response
1. **Assess Impact**: Determine scope of outage
2. **Notify Stakeholders**: Alert management and users
3. **Activate Backup**: Switch to backup systems if available
4. **Document Issue**: Log all details for analysis

#### 2. Recovery Process
1. **Identify Root Cause**: System logs, error messages
2. **Implement Fix**: Apply appropriate solution
3. **Test Functionality**: Verify all systems working
4. **Resume Operations**: Notify users of restoration
5. **Post-Incident Review**: Analyze and improve procedures

### Security Incidents

#### 1. Suspected Breach
1. **Immediate Isolation**: Disconnect affected systems
2. **Preserve Evidence**: Don't alter logs or data
3. **Notify Security Team**: Alert cybersecurity personnel
4. **Document Everything**: Detailed incident log

#### 2. Data Compromise
1. **Assess Scope**: Determine what data affected
2. **Notify Authorities**: Report to relevant agencies
3. **User Notification**: Inform affected users
4. **Remediation**: Implement security improvements

### Application Processing Issues

#### 1. System Errors
- Check error logs
- Verify database connectivity
- Restart services if needed
- Escalate to technical team

#### 2. Data Corruption
- Stop processing immediately
- Restore from latest backup
- Verify data integrity
- Resume operations carefully

---

## 📈 Performance Monitoring

### Key Performance Indicators (KPIs)

#### 1. Processing Metrics
- **Average Processing Time**: Target <7 days
- **Application Volume**: Daily/weekly trends
- **Approval Rate**: Percentage approved vs rejected
- **Error Rate**: System and user errors

#### 2. User Experience Metrics
- **Login Success Rate**: >99%
- **Application Completion Rate**: >95%
- **User Satisfaction**: Survey results
- **Support Ticket Volume**: Trend analysis

#### 3. System Performance
- **Response Time**: <2 seconds average
- **Uptime**: >99.9% availability
- **Database Performance**: Query response times
- **Storage Usage**: Capacity monitoring

### Monitoring Tools
- **System Logs**: Real-time error monitoring
- **Performance Dashboard**: Live system metrics
- **User Analytics**: Application usage patterns
- **Alert System**: Automated notifications for issues

---

## 🎓 Training & Development

### New Admin Onboarding

#### 1. Initial Training (Week 1)
- System overview and navigation
- Application review process
- User management basics
- Security protocols

#### 2. Advanced Training (Week 2)
- Report generation and analysis
- System administration
- Emergency procedures
- Performance optimization

#### 3. Ongoing Development
- Monthly training sessions
- System update briefings
- Best practice sharing
- Skill development programs

### Certification Requirements
- **Initial Certification**: Complete training program
- **Annual Recertification**: Update training and assessment
- **Specialized Certifications**: Advanced features and security

---

## 📞 Support & Escalation

### Support Levels

#### 1. Level 1 - Basic Support
- User account issues
- Application status inquiries
- Password resets
- General guidance

#### 2. Level 2 - Technical Support
- System errors
- Application processing issues
- Report generation problems
- Configuration changes

#### 3. Level 3 - Advanced Support
- Database issues
- Security incidents
- System outages
- Development requests

### Escalation Procedures
1. **Document Issue**: Complete problem description
2. **Initial Resolution**: Attempt basic troubleshooting
3. **Escalate if Needed**: Forward to appropriate level
4. **Follow Up**: Ensure resolution and user satisfaction
5. **Update Documentation**: Record solution for future reference

### Contact Information
- **Technical Support**: [Tech Support Contact]
- **Security Team**: [Security Contact]
- **Management**: [Management Contact]
- **Emergency**: [24/7 Emergency Contact]

---

## 📋 Daily Operations Checklist

### Morning Tasks (8:00 AM)
- [ ] Check system status and overnight logs
- [ ] Review pending applications queue
- [ ] Check for urgent support tickets
- [ ] Verify backup completion
- [ ] Review security alerts

### Throughout the Day
- [ ] Process applications in priority order
- [ ] Respond to user inquiries
- [ ] Monitor system performance
- [ ] Update application statuses
- [ ] Generate requested reports

### End of Day (5:00 PM)
- [ ] Complete daily processing summary
- [ ] Update management dashboard
- [ ] Secure workstation
- [ ] Document any issues or concerns
- [ ] Prepare handover notes (if applicable)

---

**Remember**: As an administrator, you are the guardian of citizen data and the efficiency of the NRC system. Always prioritize security, accuracy, and user service in your daily operations.

---

*This guide is updated regularly. Check for the latest version monthly and after any system updates.*