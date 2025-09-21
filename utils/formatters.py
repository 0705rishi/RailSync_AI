"""
Data formatting utilities for RailSync AI
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json

def format_train_status(train: Dict) -> Dict:
    """Format train data for display"""
    status_colors = {
        'On Time': 'success',
        'Delayed': 'danger', 
        'Approaching': 'warning',
        'At Platform': 'info',
        'Departed': 'secondary'
    }
    
    return {
        'id': train.get('id'),
        'name': train.get('name'),
        'status': train.get('status', 'Unknown'),
        'status_color': status_colors.get(train.get('status', 'Unknown'), 'secondary'),
        'delay_formatted': format_delay(train.get('delay_minutes', 0)),
        'speed_formatted': f"{train.get('speed', 0)} km/h",
        'route': f"{train.get('current_position', 'Unknown')} → {train.get('destination', 'Unknown')}",
        'priority_level': get_priority_text(train.get('priority', 1))
    }

def format_delay(delay_minutes: int) -> str:
    """Format delay minutes into readable string"""
    if delay_minutes == 0:
        return "On Time"
    elif delay_minutes < 60:
        return f"{delay_minutes} min late"
    else:
        hours = delay_minutes // 60
        minutes = delay_minutes % 60
        if minutes == 0:
            return f"{hours}h late"
        else:
            return f"{hours}h {minutes}m late"

def format_conflict_alert(conflict: Dict) -> Dict:
    """Format conflict data for display"""
    severity_colors = {
        'high': 'danger',
        'medium': 'warning', 
        'low': 'info'
    }
    
    severity_icons = {
        'high': 'fas fa-exclamation-triangle',
        'medium': 'fas fa-exclamation-circle',
        'low': 'fas fa-info-circle'
    }
    
    return {
        'type': conflict.get('type', '').replace('_', ' ').title(),
        'severity': conflict.get('severity', 'low'),
        'severity_color': severity_colors.get(conflict.get('severity', 'low'), 'info'),
        'severity_icon': severity_icons.get(conflict.get('severity', 'low'), 'fas fa-info-circle'),
        'description': conflict.get('description', 'Unknown conflict'),
        'trains_involved': len(conflict.get('trains', [])),
        'estimated_time': format_time_until(conflict.get('estimated_time', 0)),
        'location': conflict.get('location', 'Unknown location')
    }

def format_time_until(minutes: int) -> str:
    """Format time until event"""
    if minutes <= 0:
        return "Now"
    elif minutes == 1:
        return "1 minute"
    elif minutes < 60:
        return f"{minutes} minutes"
    else:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            return f"{hours}h {remaining_minutes}m"

def format_optimization_result(result: Dict) -> Dict:
    """Format optimization results for display"""
    return {
        'success': result.get('success', False),
        'improvements': {
            'delay_reduction': result.get('improvements', {}).get('delay_reduction', '0%'),
            'throughput_increase': result.get('improvements', {}).get('throughput_increase', '0%'),
            'conflicts_resolved': result.get('improvements', {}).get('conflicts_resolved', 0),
            'efficiency_gain': result.get('improvements', {}).get('efficiency_gain', '0%')
        },
        'recommendations_count': len(result.get('optimized_schedule', [])),
        'processing_time': result.get('processing_time', 0),
        'confidence_score': result.get('confidence_score', 0)
    }

def format_metrics_dashboard(metrics: Dict) -> Dict:
    """Format metrics for dashboard display"""
    return {
        'total_trains': {
            'value': metrics.get('total_trains', 0),
            'formatted': str(metrics.get('total_trains', 0)),
            'icon': 'fas fa-train',
            'color': 'primary'
        },
        'active_conflicts': {
            'value': metrics.get('active_conflicts', 0),
            'formatted': str(metrics.get('active_conflicts', 0)),
            'icon': 'fas fa-exclamation-triangle',
            'color': 'warning' if metrics.get('active_conflicts', 0) > 0 else 'success'
        },
        'average_delay': {
            'value': metrics.get('average_delay', 0),
            'formatted': f"{metrics.get('average_delay', 0):.1f} min",
            'icon': 'fas fa-clock',
            'color': 'info'
        },
        'system_efficiency': {
            'value': metrics.get('system_efficiency', 0),
            'formatted': f"{metrics.get('system_efficiency', 0)}%",
            'icon': 'fas fa-tachometer-alt',
            'color': 'success' if metrics.get('system_efficiency', 0) >= 80 else 'warning'
        },
        'throughput_today': {
            'value': metrics.get('throughput_today', 0),
            'formatted': str(metrics.get('throughput_today', 0)),
            'icon': 'fas fa-chart-line',
            'color': 'secondary'
        }
    }

def get_priority_text(priority: int) -> str:
    """Convert numeric priority to text"""
    priority_map = {
        1: 'Low',
        2: 'Medium', 
        3: 'High',
        4: 'Very High',
        5: 'Critical'
    }
    return priority_map.get(priority, 'Unknown')

def format_json_response(data: Any, success: bool = True, message: str = "") -> str:
    """Format data as JSON response"""
    response = {
        'success': success,
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    
    if message:
        response['message'] = message
    
    return json.dumps(response, indent=2, default=str)

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format number as percentage"""
    return f"{value:.{decimals}f}%"

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable format"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_currency(amount: float, currency: str = "₹") -> str:
    """Format amount as currency"""
    return f"{currency}{amount:,.2f}"