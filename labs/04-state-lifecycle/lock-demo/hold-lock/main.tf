resource "time_sleep" "lock_holder" {
  create_duration = "45s"
}

output "lock_demo" {
  description = "Confirma que a operação que ocupou o lock terminou."
  value       = "lock liberado após a operação"
  depends_on  = [time_sleep.lock_holder]
}
