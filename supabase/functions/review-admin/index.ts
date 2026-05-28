import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  try {
    const { action, id, password } = await req.json();
    const adminPassword = Deno.env.get('ADMIN_PASSWORD');
    if (!adminPassword || password !== adminPassword) return json({ error: 'Unauthorized' }, 401);

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    );

    if (action === 'list') {
      const { data, error } = await supabase
        .from('div_review')
        .select('*')
        .order('created_at', { ascending: false });
      if (error) throw error;
      return json(data);
    }
    if (action === 'approve' || action === 'reject') {
      const { error } = await supabase
        .from('div_review')
        .update({ approved: action === 'approve' })
        .eq('id', id);
      if (error) throw error;
      return json({ ok: true });
    }
    if (action === 'delete') {
      const { error } = await supabase
        .from('div_review')
        .delete()
        .eq('id', id);
      if (error) throw error;
      return json({ ok: true });
    }
    return json({ error: 'Unknown action' }, 400);
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
});
