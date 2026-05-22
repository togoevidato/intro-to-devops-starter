output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  value = aws_ecs_service.app.name
}

output "rds_endpoint" {
  value = aws_db_instance.mysql.address
}

output "cloudwatch_log_group" {
  value = aws_cloudwatch_log_group.app.name
}

output "alb_dns_name" {
  value = aws_lb.app.dns_name
}

output "alb_url" {
  value = "http://${aws_lb.app.dns_name}"
}

output "target_group_arn" {
  value = aws_lb_target_group.app.arn
}