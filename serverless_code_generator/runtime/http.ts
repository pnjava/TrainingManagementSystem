export function buildResponse(status: number, body: any) {
  return { statusCode: status, body: JSON.stringify(body) };
}
