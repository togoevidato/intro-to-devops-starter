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