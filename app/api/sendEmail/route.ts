// Contact form retired: it only attracted bot spam. No email is sent.
export async function POST() {
  return new Response('Contact form is no longer available', { status: 410 });
}
