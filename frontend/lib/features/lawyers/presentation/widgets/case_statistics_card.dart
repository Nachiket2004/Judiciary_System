import 'package:flutter/material.dart';

class CaseStatisticsCard extends StatelessWidget {
  final int totalCases;
  final int wonCases;
  final double winRate;

  const CaseStatisticsCard({
    super.key,
    required this.totalCases,
    required this.wonCases,
    required this.winRate,
  });

  @override
  Widget build(BuildContext context) {
    final lostCases = totalCases - wonCases;
    
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Case Statistics',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            
            // Statistics grid
            Row(
              children: [
                Expanded(
                  child: _buildStatCard(
                    context,
                    'Total Cases',
                    totalCases.toString(),
                    Icons.gavel,
                    Colors.blue,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildStatCard(
                    context,
                    'Won Cases',
                    wonCases.toString(),
                    Icons.check_circle,
                    Colors.green,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            
            Row(
              children: [
                Expanded(
                  child: _buildStatCard(
                    context,
                    'Lost Cases',
                    lostCases.toString(),
                    Icons.cancel,
                    Colors.red,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildStatCard(
                    context,
                    'Win Rate',
                    '${winRate.toStringAsFixed(1)}%',
                    Icons.trending_up,
                    _getWinRateColor(winRate),
                  ),
                ),
              ],
            ),
            
            if (totalCases > 0) ...[
              const SizedBox(height: 16),
              _buildProgressBar(context),
            ],
            
            if (totalCases == 0) ...[
              const SizedBox(height: 16),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  children: [
                    Icon(
                      Icons.info_outline,
                      color: Colors.grey.shade600,
                      size: 32,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'No cases added yet',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        color: Colors.grey.shade600,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Add your case history to build your profile',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: Colors.grey.shade600,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(
    BuildContext context,
    String label,
    String value,
    IconData icon,
    Color color,
  ) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color.withOpacity(0.2)),
      ),
      child: Column(
        children: [
          Icon(
            icon,
            color: color,
            size: 24,
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            label,
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
              color: Colors.grey.shade600,
              fontWeight: FontWeight.w500,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildProgressBar(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Case Outcome Distribution',
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 8),
        
        // Win rate progress bar
        Row(
          children: [
            Expanded(
              child: LinearProgressIndicator(
                value: winRate / 100,
                backgroundColor: Colors.red.shade200,
                valueColor: AlwaysStoppedAnimation<Color>(Colors.green.shade600),
                minHeight: 8,
              ),
            ),
            const SizedBox(width: 12),
            Text(
              '${winRate.toStringAsFixed(1)}%',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                fontWeight: FontWeight.w600,
                color: _getWinRateColor(winRate),
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        
        // Legend
        Row(
          children: [
            _buildLegendItem(context, 'Won', Colors.green.shade600),
            const SizedBox(width: 16),
            _buildLegendItem(context, 'Lost', Colors.red.shade600),
          ],
        ),
      ],
    );
  }

  Widget _buildLegendItem(BuildContext context, String label, Color color) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 12,
          height: 12,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
          ),
        ),
        const SizedBox(width: 4),
        Text(
          label,
          style: Theme.of(context).textTheme.bodySmall?.copyWith(
            color: Colors.grey.shade600,
          ),
        ),
      ],
    );
  }

  Color _getWinRateColor(double winRate) {
    if (winRate >= 80) return Colors.green.shade600;
    if (winRate >= 60) return Colors.orange.shade600;
    return Colors.red.shade600;
  }
}