import 'package:flutter/material.dart';

class ProfileInfoCard extends StatelessWidget {
  final Map<String, dynamic> profile;

  const ProfileInfoCard({
    super.key,
    required this.profile,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Profile Information',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            
            _buildInfoRow(
              context,
              'Email',
              profile['email'] ?? 'Not provided',
              Icons.email_outlined,
            ),
            
            _buildInfoRow(
              context,
              'Bar ID',
              profile['bar_id'] ?? 'Not provided',
              Icons.badge_outlined,
            ),
            
            _buildInfoRow(
              context,
              'Specialization',
              profile['specialization'] ?? 'General Practice',
              Icons.work_outline,
            ),
            
            _buildInfoRow(
              context,
              'Experience',
              '${profile['experience_years'] ?? 0} years',
              Icons.timeline_outlined,
            ),
            
            _buildInfoRow(
              context,
              'Location',
              profile['location'] ?? 'Not specified',
              Icons.location_on_outlined,
            ),
            
            if (profile['contact_phone'] != null && profile['contact_phone'].toString().isNotEmpty)
              _buildInfoRow(
                context,
                'Phone',
                profile['contact_phone'],
                Icons.phone_outlined,
              ),
            
            if (profile['consultation_fee'] != null)
              _buildInfoRow(
                context,
                'Consultation Fee',
                '₹${profile['consultation_fee']}',
                Icons.currency_rupee_outlined,
              ),
            
            if (profile['bio'] != null && profile['bio'].toString().isNotEmpty) ...[
              const SizedBox(height: 16),
              Text(
                'About',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                profile['bio'],
                style: Theme.of(context).textTheme.bodyMedium,
              ),
            ],
            
            if (profile['office_address'] != null && profile['office_address'].toString().isNotEmpty) ...[
              const SizedBox(height: 16),
              Text(
                'Office Address',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                profile['office_address'],
                style: Theme.of(context).textTheme.bodyMedium,
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(BuildContext context, String label, String value, IconData icon) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            icon,
            size: 20,
            color: Colors.grey.shade600,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Colors.grey.shade600,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  value,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}